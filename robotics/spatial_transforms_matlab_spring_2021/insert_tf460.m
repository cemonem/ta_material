function [tf460_internals, result] = insert_tf460(tf460_internals, from, to, T)
%INSERT_TF460 insert a transformation between indices
%   This function inserts a 4x4 3D homogeneous transformation T to the
%   query system, which represents pose of "to" with respect to "from". If
%   there is a previous entry or the relationship is implied from other
%   transforms, the operation should be rejected.
%   "from" and "to" are integers from 0 to 10.
%   result is false if the operation is rejected and true otherwise.
%   tf460_internals value is a struct for storing the internals
%   of the query system. MATLAB does not support call by reference, so we
%   have to explicitly return it.


% structs in matlab are similar to javascript objects. Just assign a
% value to a field and voila.
    tf460_internals.something_inserted = true;
end

