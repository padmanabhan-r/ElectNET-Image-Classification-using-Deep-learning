import React from 'react';
import { BrowserRouter, Route } from 'react-router-dom'
import AppContainer from '../containers/AppContainer';
import ResultContainer from '../containers/ResultContainer';
import LoadingContainer from '../containers/LoadingContainer';

class AppRouter extends React.Component {
	render() {
		return (
				<BrowserRouter>
					<div>
						<Route exact path="/" component={AppContainer} />
						<Route path="/loading" component={LoadingContainer} />
						<Route path="/result" component={ResultContainer} />
					</div>
				</BrowserRouter>
		);
	}
}

export default AppRouter;
