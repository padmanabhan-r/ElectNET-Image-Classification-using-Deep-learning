import React, { Component } from 'react';
import { connect } from 'react-redux';
import Result from '../components/Result'

class ResultContainer extends Component {
	render() {
		return (
			<Result {...this.props} />
		)
	}
}

const mapStateToProps = (state) => state

const mapDispatchToProps = (dispatch) => ({

})
export default connect(mapStateToProps, mapDispatchToProps)(ResultContainer);