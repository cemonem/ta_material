%% some simple example transforms
A = eye(4);
A(1:3, 1:3) = rotx(pi/2);
A(1:3, 4) = [1 2 3];
B = A;
B(1:3, 4) = [2 3 4];
C = eye(4);
C(1:3, 4) = [1 1 1];
D = eye(4);
D(1:3, 1:3) = rotx(-pi/2);
E = eye(4);
E(1:3, 1:3) = rotx(pi/2);
%% enter some information
tf460 = init_tf460();
[tf460, ~] = insert_tf460(tf460, 0, 1, A);
[tf460, ~] = insert_tf460(tf460, 1, 2, C);
[tf460, ~] = insert_tf460(tf460, 0, 3, B);
[tf460, ~] = insert_tf460(tf460, 5, 4, D);
%% query some transforms
[tf460, tf] = query_tf460(tf460, 6, 6);
disp('this should be identity matrix');
tf

[tf460, tf] = query_tf460(tf460, 7, 8);
disp('this should be [], not enough info to calculate');
tf

[tf460, tf] = query_tf460(tf460, 0, 7);
disp('this should be [], not enough info to calculate');
tf

[tf460, tf] = query_tf460(tf460, 0, 2);
disp('this should be equal to B');
tf

[tf460, tf] = query_tf460(tf460, 2, 3);
disp('this should be identity matrix');
tf

[tf460, tf] = query_tf460(tf460, 2, 5);
disp('this should be [], not enough info to calculate');
tf

%% enter more transforms
[tf460, result] = insert_tf460(tf460, 2, 3, A);
disp('this should be false, 2-to-3 is eye(4), cannot insert new value')
result

[tf460, result] = insert_tf460(tf460, 4, 1, E);
disp('should be true, this information is new')
result

%% more queries
[tf460, tf] = query_tf460(tf460, 2, 5);
disp('now this should have a result, should be a translation by [-1 -1 -1]');
tf
