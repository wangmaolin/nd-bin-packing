import numpy as np
import cvxpy as cvx
import cylp
from timeit import default_timer as time

def skip_condense(vt_bit_map):
	vec_length = vt_bit_map.shape[0]
	vt_loc_map = np.array(range(vec_length), dtype=np.uint32)
	return vt_loc_map

def brute_force_condense(vt_bit_map):
	vec_length = vt_bit_map.shape[0]
	""" the location of vector after condensing"""
	vt_loc_map = np.ones(vec_length, dtype=np.uint32)*-1
	condense_bitmap = np.zeros_like(vt_bit_map)
	max_loc_after_condense = 1

	for i in range(vec_length):
		bit_map_single= vt_bit_map[i,:]

		all_full_flag = True
		for j in range(max_loc_after_condense):
			bit_map_to_merge = condense_bitmap[j,:]	
			bit_map_after_merge = bit_map_single + bit_map_to_merge
			if np.any(bit_map_after_merge > 1):
				continue
			else:
				all_full_flag = False
				condense_bitmap[j,:]=bit_map_after_merge
				vt_loc_map[i]=j

		if all_full_flag:
			condense_bitmap[max_loc_after_condense,:]=bit_map_single
			vt_loc_map[i]=max_loc_after_condense
			max_loc_after_condense += 1

	print('N_BOXES USED: ', np.max(vt_loc_map)+1)

	return vt_loc_map

def cvx_condense(vt_bit_map):
	"""Data"""
	M_CONSTRAINS = vt_bit_map.shape[1]

	box_vol_limit = 1

	N_ITEMS = vt_bit_map.shape[0]
	max_n_boxes = N_ITEMS 

	""" Optimization """
	M = N_ITEMS + 1

	""" VARIABLES """
	box_used = cvx.Variable(max_n_boxes, boolean=True)
	box_item_map = cvx.Variable((max_n_boxes, N_ITEMS), boolean=True)

	"""CONSTRAINTS"""
	cons = []

	"""each item is shipped once"""
	cons.append(cvx.sum(box_item_map, axis=0) == 1)

	"""box is used when >=1 item is using it"""
	cons.append(box_used * M >= cvx.sum(box_item_map, axis=1))

	""" box vol constraints """
	for i in range(M_CONSTRAINS):
		cons.append(box_item_map * vt_bit_map[:,i] <= box_vol_limit)

	problem = cvx.Problem(cvx.Minimize(cvx.sum(box_used)), cons)
	start_t = time()
	problem.solve(solver='CBC', verbose=True)
	end_t = time()
	print('time used (cvxpys reductions & solving): ', end_t - start_t)
	print(problem.status)

	""" Reconstruct solution """
	n_boxes_used = int(np.round(problem.value))

	print('N_BOXES USED: ', n_boxes_used)
	# print(box_item_map.value)

	""" the location of vector after condensing"""
	vt_loc_map = np.ones(N_ITEMS, dtype=np.int32)*-1
	""" Recover the way of packing"""
	for i in range(box_item_map.value.shape[0]):
		rows_in_the_same_box = np.array(box_item_map.value[i,:],dtype=bool)
		vt_loc_map[rows_in_the_same_box]=i

	return vt_loc_map
