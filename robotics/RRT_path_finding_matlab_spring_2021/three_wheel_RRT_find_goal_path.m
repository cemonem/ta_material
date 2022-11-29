function [goal_path] = three_wheel_RRT_find_goal_path(tree, p_goal)
%THREE_WHEEL_RRT_FIND_GOAL_PATH finds the path from the root of the tree to
%the configuration q with close(q(1:2),p_goal) = true.
%goal_path is an 3xn array if there are n nodes within the path
%each column is a configuration [x y theta] (in global coords)
%with goal_path(:,1) = tree.value and close(goal_path(:,n),p_goal) = true.
%goal_path = [] if there is no configuration q with close(q(1:2),p_goal) =
%true.

% your implementation here

end


function [result] = close(q,p)
    result = (q(1)-p(1))^2+(q(2)-p(2))^2 < 0.001;
end

