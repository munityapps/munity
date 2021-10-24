import logo from '../../../assets/logo.png';
import { ProgressSpinner } from 'primereact/progressspinner';

const LoadingApp = () => {
	return <div className="app-loading">
		<img src={logo} alt="Logo" />
		<ProgressSpinner />
	</div>;
}

export default LoadingApp;