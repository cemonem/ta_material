function [tf460_internals, T] = query_tf460(tf460_internals, from, to)
%QUERY_TF460 query 4x4 3D homogeneous transformations
%   Calculates the 4x4 3D homogeneous transform of "to" w.r.t. "from".
%   "from" and "to" are integers from 0 to 10.
%   T is the 4x4 transformation matrix. If it is not possible to calculate
%   T, T is returned as an empty array.
%   tf460_internals value is a struct for storing the internals
%   of the query system. MATLAB does not support call by reference, so we
%   have to explicitly return it.

    T = [];
end
