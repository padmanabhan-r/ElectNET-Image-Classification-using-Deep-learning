import { combineReducers } from 'redux';
import imageUploader from './imageUploader';
import results from './results';

export default combineReducers({
	imageUploader,
	results
});