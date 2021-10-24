
import 'react-toastify/dist/ReactToastify.css';
import LayoutDispatcher from '../core/components/LayoutDispatcher';
import Navbar from '../layouts/components/Navbar';
import OvermindWorkspaces from './components/workspaces';

const Overmind = () => {
	return <LayoutDispatcher
		layoutName="LayoutOvermind"
		navbarSlot={<Navbar workspace={null}/>}
		mainSlot={<OvermindWorkspaces/>}
	/>
}

export default Overmind;