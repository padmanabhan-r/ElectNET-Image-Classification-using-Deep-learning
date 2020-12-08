import React, { Component } from 'react';
import { connect } from 'react-redux';
import Loading from '../components/Loading'
import { fetchResults } from '../actions/resultActions'

class LoadingContainer extends Component {
	render() {
		return (
			<Loading {...this.props} />
		)
	}
}

const mapStateToProps = (state) => state

const mapDispatchToProps = (dispatch) => ({

	fetchResults: (directory) => {
		dispatch(fetchResults(directory))
	}

})
export default connect(mapStateToProps, mapDispatchToProps)(LoadingContainer);
