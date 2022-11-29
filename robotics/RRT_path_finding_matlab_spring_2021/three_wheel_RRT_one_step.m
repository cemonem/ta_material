function [tree,q_new] = three_wheel_RRT_one_step(tree, p_goal, params)
%THREE_WHEEL_RRT_ONE_STEP adds a node to the RRT. tree is the RRT to be
%extended, in the form of the struct tree_init constructs, containing nodes
%that hold 3x1 arrays of [x y theta]' as values (as the global configuration of the robot)
%p_goal is the 2x1 array [x y]' (global coordinates of the goal position). 
%params is a struct containing map, robot, and misc. algorithm parameters (see three_wheel_RRT_example).
%q_new is the node newly added to the tree.
    q_new = [];
    while(isempty(q_new))
        p_rand = rand_conf(p_goal, params);
        [q_near, ~] = nearest_vertex(p_rand, tree);
        q_new = steer(q_near, p_rand, params);
        if ~isempty(q_new) & collision_free(q_new, params)
            tree = attach(q_new,q_near,tree);
        else
            q_new = [];
        end
    end
end

function [tree] = attach(q_new, q_near, tree)
%ATTACH attaches q_new to all of the nodes having the value q_near.
    if tree.value == q_near
        tree.children = [tree.children tree_init(q_new)];
    end

    %matlab is call by value! that's why attaching is a little bit
    %complicated
    new_children = [];
    for child = tree.children
        new_children = [new_children attach(q_new, q_near, child)];
    end
    tree.children = new_children;
end

function p_rand = rand_conf(p_goal, params)
%RAND_CONF samples a 2x1 position [x y] in global coordinates that does not collide
%with the obstacles. p_goal is sampled with probability params.epsilon,
%with probability 1-params.epsilon, it is sampled uniformly within the free
%parts of the rectangle defined by params.xlim and params.ylim
    if params.epsilon < rand()
        colfree = false;
        while(~colfree)
            q_rand_x = params.xlim(1)+rand()*(params.xlim(2)-params.xlim(1));
            q_rand_y = params.ylim(1)+rand()*(params.ylim(2)-params.ylim(1));
            p_rand = [q_rand_x q_rand_y]';
            colfree = collision_free(p_rand, params);
        end
    else
        p_rand = p_goal;
    end
end

function [q_near, dist_near] = nearest_vertex(p, tree)
%NEAREST_VERTEX finds the nearest vertex of tree to the position p (an 2x1 array as global coords [x y]').
%q_near is the value of the closest vertex.
%dist_near is the value of the closest distance.
%Let q be the value of an arbitrary vertex.
%distance function between q and p is simply L2 norm:
%sqrt((q(1)-p(1))^2+(q(2)-p(2))^2)

%your implementation here

end

function q_new = steer(q_near, p, params)
%STEER moves toward p from q_near by param.step_size using local_planner.
%if a trajectory towards p is not possible (exists is false, defined in
%local_planner description), q_new = [].
%simply substitute t in the parametric trajectory local_planner implies
%with params.step_size. If param.step_size > t_final (t_final defined in local_planner
%description), substitute t_final for t.
%q_near is a full configuration as a 3x1 array [x y theta]' (in global
%coords)
%p is a position as a 2x1 array [x y]' (in global coords)
%q_new is the new configuration reached from q_near when moving towards p
%by min(params.step_size,t_final) as a 3x1 array [x y theta]'. Its
%orientation depends on  min(params.step_size,t_final) and q_near(3).

% your implementation here

end

function result = collision_free(q, params)
%COLLISION_FREE checks whether the configuration/position is in a valid place in the map.
%returns true if this configuration/position is valid.
    result = true;
    if q(1)-params.r < params.xlim(1) | q(1)+params.r > params.xlim(2)... 
        | q(2)-params.r < params.ylim(1) | q(2)+params.r > params.ylim(2)
        result = false;
        return
    end
    for map_circ = params.map
        m_x = map_circ(1);
        m_y = map_circ(2);
        m_r = map_circ(3);
        if m_r+params.r > sqrt((m_x-q(1))^2+(m_y-q(2))^2)
            result = false;
            return
        end
    end
end