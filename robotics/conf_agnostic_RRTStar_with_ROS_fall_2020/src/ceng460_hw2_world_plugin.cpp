#include <gazebo/common/Plugin.hh>
#include <ros/ros.h>
#include <boost/bind.hpp>
#include <boost/thread.hpp>
#include <boost/thread/mutex.hpp>
#include <ros/callback_queue.h>
#include <gazebo/common/Events.hh>
#include <gazebo/physics/physics.hh>
#include <gazebo/transport/transport.hh>
#include <std_srvs/Trigger.h>

namespace gazebo
{
class Ceng460Hw2WorldPlugin : public WorldPlugin
{
private:
  ros::NodeHandle nh;
  boost::thread service_callback_queue_thread;
  ros::CallbackQueue service_callback_queue;
  ros::ServiceServer service_server_handle; //if it goes out of scope service terminates
  event::ConnectionPtr update_connection_handle; //if it goes out of scope no update callbacks happen
  bool trig;
  bool attach_success;
  bool attached;
  boost::mutex mutex;
  physics::WorldPtr world;
  ignition::math::Pose3d hw2_object_relative_pose;
  gazebo::transport::NodePtr gazebo_node_handle;
  gazebo::transport::SubscriberPtr contact_sub_callback_handle;
  physics::ModelPtr hw2_object;
  boost::condition_variable condition;
  ignition::math::Pose3d ee_link_wrt_wrist_3_link;
  ignition::math::Pose3d ideal_obj_wrt_ee_link;

public:
  Ceng460Hw2WorldPlugin() : WorldPlugin()
  {
  }

  void Load(physics::WorldPtr _world, sdf::ElementPtr _sdf)
  {
    ee_link_wrt_wrist_3_link.Pos().Y() = 0.0823;
    ee_link_wrt_wrist_3_link.Rot().Euler(0,0,IGN_PI_2);

    ideal_obj_wrt_ee_link.Pos().X() = 0.1;
    ideal_obj_wrt_ee_link.Rot().Euler(IGN_PI,0,IGN_PI_2);


    // Make sure the ROS node for Gazebo has already been initialized
    if (!ros::isInitialized())
    {
      ROS_FATAL_STREAM("A ROS node for Gazebo has not been initialized, unable to load plugin. "
        << "Load the Gazebo system plugin 'libgazebo_ros_api_plugin.so' in the gazebo_ros package)");
      return;
    }
    
    double hw2_object_x = nh.param("hw2_object/init_pose/x",0.0);
    double hw2_object_y = nh.param("hw2_object/init_pose/y",0.0);
    double hw2_object_z = nh.param("hw2_object/init_pose/z",0.0);

    world = _world;

    hw2_object = world->ModelByName("hw2_object");
    if(hw2_object == nullptr)
    {
      ROS_FATAL_STREAM("No hw2_object model in SDF File!");
      return;
    }

    ignition::math::Pose3d initial_pose;
    initial_pose.Pos().X() = hw2_object_x;
    initial_pose.Pos().Y() = hw2_object_y;
    initial_pose.Pos().Z() = hw2_object_z;
    hw2_object->SetWorldPose(initial_pose);

    gazebo_node_handle = gazebo::transport::NodePtr(new transport::Node());
    gazebo_node_handle->Init(world->Name());
    contact_sub_callback_handle = gazebo_node_handle->Subscribe("~/physics/contacts", &Ceng460Hw2WorldPlugin::ContactsSubscriberCallback, this);
    //for some reason you need to subscribe to receive contacts???
    //https://answers.gazebosim.org//question/12317/some-contacts-not-detected/

    ros::AdvertiseServiceOptions aso;
    boost::function<bool(std_srvs::Trigger::Request&, std_srvs::Trigger::Response&)> service_callback = 
      boost::bind(&Ceng460Hw2WorldPlugin::AttachObjectServiceCallback, this, _1, _2);
    aso.init("gazebo/attach_object", service_callback);
    aso.callback_queue = &service_callback_queue;
    service_server_handle = nh.advertiseService(aso);

    service_callback_queue_thread = boost::thread(boost::bind(&Ceng460Hw2WorldPlugin::ServiceCallbackQueueThread, this));

    this->update_connection_handle = event::Events::ConnectWorldUpdateBegin(
      boost::bind(&Ceng460Hw2WorldPlugin::OnWorldBeginUpdate, this));
  }

  void ContactsSubscriberCallback(ConstWorldStatisticsPtr &_msg)
  {
  }

  void ServiceCallbackQueueThread()
  {
    while(nh.ok())
    {
      service_callback_queue.callAvailable();
    }
  }

  void OnWorldBeginUpdate()
  {
    boost::mutex::scoped_lock lock(mutex);

    std::vector<gazebo::physics::Contact *> contacts = world->Physics()->GetContactManager()->GetContacts();
    int contact_count = world->Physics()->GetContactManager()->GetContactCount();
    for(int i = 0; i < contact_count; i++)
    {
      gazebo::physics::Contact * contact = contacts[i];
      if(contact->collision1->GetModel() != contact->collision2->GetModel())
      {
        ROS_WARN_STREAM("Collision Detected! Contact " << i+1 <<"/"<< contact_count <<" DebugStr: " << contacts[i]->DebugString());
      }
    }

    hw2_object->ResetPhysicsStates();

    physics::ModelPtr robot = world->ModelByName("robot");

    if(robot == nullptr)
    {
      trig = false;
      attach_success = false;
      condition.notify_all();
      return;
    }

    physics::LinkPtr robot_wrist_3_link = robot->GetLink("wrist_3_link");

    if(trig)
    {
      if(attached)
      {
        attached = false;
        attach_success = true;
      }
      else
      {
        ignition::math::Pose3d rel_pose = hw2_object->WorldPose()-(ee_link_wrt_wrist_3_link+robot_wrist_3_link->WorldPose());
        attached = all_close(rel_pose, ideal_obj_wrt_ee_link);
        if(!attached) ROS_WARN_STREAM("Relative pose is not ideal, cannot attach! in x y z roll pitch yaw, relative pose: " << rel_pose << " ideal pose: " << ideal_obj_wrt_ee_link);
        attach_success = attached;
      }
    }
    
    if(attached)
    {
      if(trig) hw2_object_relative_pose = hw2_object->WorldPose()-robot_wrist_3_link->WorldPose();
      hw2_object->SetWorldPose(hw2_object_relative_pose+robot_wrist_3_link->WorldPose());
      hw2_object->ResetPhysicsStates();
    }
    
    trig = false;
    condition.notify_all();
  }

  bool all_close(ignition::math::Pose3d& first, ignition::math::Pose3d& second)
  {
    // https://math.stackexchange.com/questions/90081/quaternion-distance
    double quaternion_distance =  1- (first.Rot().Dot(second.Rot()))*(first.Rot().Dot(second.Rot()));
    //cannot be larger than 8 degrees (1-cos(8))/2) is about 0.005
    return first.Pos().Distance(second.Pos()) < 0.05 && quaternion_distance < 0.005;
  }

  bool AttachObjectServiceCallback(std_srvs::Trigger::Request& req, std_srvs::Trigger::Response& resp)
  {
    boost::mutex::scoped_lock lock(mutex);
    trig = true;
    ROS_INFO_STREAM("attach_object service called.");
    while(trig) condition.wait(lock);
    ROS_INFO_STREAM("attach_object service returning: " << attach_success);
    resp.success = attach_success;
    return true;
  }

  protected:
  virtual void FiniChild() {
    service_callback_queue.clear();
    service_callback_queue.disable();
    nh.shutdown();
    service_callback_queue_thread.join();
  }

};
GZ_REGISTER_WORLD_PLUGIN(Ceng460Hw2WorldPlugin)
}