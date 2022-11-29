function [] = tree_print_dfs(tree)
%TREE_PRINT prints the tree with DFS algorithm. assumes elements are [3x1]
%arrays.
    tree_print_dfs_helper(0,tree) % the arguments of the helper func helps us remember 
    % the current depth of the tree. It is a good method to transfer info
    % from caller to callee in recursive algorithms. You can do the
    % same with return values when you want to transfer info from callee to
    % caller.
end

function [] = tree_print_dfs_helper(depth, tree)

% visit (print) parent first. some pretty printing here according to depth
fprintf([repmat(repmat(' ',1,12),1,depth),'[%1.1f,%1.1f,%1.1f]\n'],tree.value(1),tree.value(2),tree.value(3));

% then recursively print children trees
for child = tree.children
    tree_print_dfs_helper(depth+1, child) % then recursively visit children
end

end

