%%
SEED = 4602022;
rng(SEED); % fix a seed for rng for easy debugging
params = struct(); % params of robot and the environment
%easy_map
%params.xlim = [1.5 5]; % a 2d area bounded within xlim and ylim
%params.ylim = [2 7];
%params.map = [[3 3 1]; [5.2 5 1];[2 6.5 2]]'; % obstacles are filled
%circles as a list of columns [x y r]'
params.xlim = [0 5];
params.ylim = [0 5];
params.r = 0.25; %robot body radius
params.map = [[1.5 0.5 0.5];[1.5 1.5 0.5];[1.5 2.5 0.5];[1.5 3.5 0.5];
    [3.5 1.5 0.5];[3.5 2.5 0.5];[3.5 3.5 0.5];[3.5 4.5 0.5]]';
params.epsilon = 0.15; %probability of sampling goal point
params.step_size = 0.3; %step_size in RRT algorithm, corresponds to length of the arc robot draws here
%%
%easy_map
%tree = tree_init([1.7 2.2 0.3]');
tree = tree_init([0.5 0.5 0.3]');
p_goal = [4.5 4.5]';
num_nodes = 0;
while(true)
%for i = 1:100 % set 1,2,3 to debug easily
    [tree,q_new] = three_wheel_RRT_one_step(tree, p_goal, params);
    num_nodes = num_nodes+1;
    %uncomment to animate :)
    %clf;
    %ax = gca();
    %three_wheel_RRT_draw(ax,tree,p_goal,goal_path,params);
    %pause(0.1);
    if (q_new(1)-p_goal(1))^2+(q_new(2)-p_goal(2))^2 < 0.001
        fprintf("Goal pt found, Number of Nodes: %d\n",num_nodes);
        break
    end

end
goal_path = three_wheel_RRT_find_goal_path(tree, p_goal);
clf;
ax = gca();
three_wheel_RRT_draw(ax,tree,p_goal,goal_path,params);
%%
% set(gcf,'Units','inches');
% screenposition = get(gcf,'Position');
% set(gcf,...
%     'PaperPosition',[0 0 screenposition(3:4)],...
%     'PaperSize',[screenposition(3:4)]);
% print(gcf,'sneak_peek','-dpdf','-r0');

