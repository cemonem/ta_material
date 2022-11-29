function [tree] = tree_add_child(tree, child_tree)
%TREE_ADD_CHILD example for adding child to a tree, one would use this
%function as
%tree = tree_init(3);
%tree = tree_add_child(tree, tree_init(5));
%if i did
%tree_add_child(tree, tree_init(5)); without assigning nothing would happen
%matlab is call by value!
tree.children = [tree.children child_tree];
end

