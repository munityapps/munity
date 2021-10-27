import { useDispatch, useSelector } from 'react-redux';
// Use throughout your app instead of plain `useSelector`
export var useAppSelector = useSelector;
export var useAppDispatch = function () { return useDispatch(); };
