import imageConstants from '../constants/imageConstants'

const initialState = {
	result_success: false,
	result_data: []
}

export default (state = initialState, action={}) => {
	switch (action.type) {
		case imageConstants.RESULTS_SUCCESS:
			return {
				...state,
				...{
					result_success: true,
					result_data: action.payload
				}
			}
		default:
			return state
	}
}