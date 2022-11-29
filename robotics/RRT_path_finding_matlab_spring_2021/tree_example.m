%%
a = tree_init([3,4,pi/2]);
b = tree_init([2,3,0]);
c = tree_init([1,5,0.2]);
d = tree_init([0,0,0.3]);
e = tree_init([0,4,0.5]);

f = tree_add_child(c,d); % c won't change, matlab funcs are call by value!!!
f = tree_add_child(f,c);
f = tree_add_child(b,f); % won't cause an infinite tree. matlab funcs are call by value!!!
g = tree_add_child(a,b);
h = tree_init([0,0,0]);
h = tree_add_child(h,g);
h = tree_add_child(h,e);
h = tree_add_child(h,b);
h = tree_add_child(h,h);
h = tree_add_child(h,f);
%%
tree_print_dfs(h);
%%
tree_print_bfs(h);
