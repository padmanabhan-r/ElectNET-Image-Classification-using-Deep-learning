import React, { Component } from 'react';
import '../styles/app.css';

class ResultItem extends Component {
	
	render() {
		return (
			<div className="section">
				<div className="image-container">
					<img src={this.props.image} className="image-section" alt="provided" />
				</div>
				<div className="section-desc">
					<p className="section-text"><span className="section-title">Category:</span> {this.props.category}</p>
				</div>
			</div>
		);
	}
}

export default ResultItem;
