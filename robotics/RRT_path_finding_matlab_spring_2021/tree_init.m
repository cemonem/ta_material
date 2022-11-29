function [root] = tree_init(value)
%TREE_INIT construct a tree
root = struct('value',value,'children',[]);
end

