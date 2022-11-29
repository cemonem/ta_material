function [] = tree_print_bfs(tree)
%TREE_PRINT_BFS  prints the tree with BFS algorithm (depth n-1 printed
%before depth n) assumes elements are [3x1] arrays
queue = {{tree,0}}; % put the depth here as well to go to a newline when
%appropriate. You can extend this algorithm by basically putting extra
%things to your queue when you want info transferred from parents to
%children.

prev_depth = 0;
result = '';
while ~isempty(queue)
    top = queue{1};
    queue = queue(2:end);
    tree = top{1};
    depth = top{2};
    if prev_depth < depth
        result = [result(1:end-1) '\n']; % nodes with a certain depth are over, go to next line
        prev_depth = depth;
    end
    result = [result sprintf('[%1.1f,%1.1f,%1.1f] ', tree.value(1),tree.value(2),tree.value(3))];
    for child = tree.children
        queue{end+1} = {child,depth+1};
    end
    
end
fprintf([result '\n']);
