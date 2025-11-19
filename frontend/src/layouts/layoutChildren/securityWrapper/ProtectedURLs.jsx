import { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { checkAuthStatus, initializeAuth } from '@redux/auth/authSlice';
import { Outlet, useNavigate } from 'react-router-dom';
import { setStatus } from '@redux/status/statusSlice';

function ProtectedURLs() {
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const { isAuthenticated, status, token, user } = useSelector((state) => state.auth);

  // Initialize auth from localStorage on component mount
  useEffect(() => {
    dispatch(initializeAuth());
  }, [dispatch]);

  useEffect(() => {
    // Only check auth status if we have a token
    if (token) {
      dispatch(checkAuthStatus());
    }
  }, [dispatch, token]);

  useEffect(() => {
    if (status === 'error' || (!isAuthenticated && status === 'succeeded' && !token)) {
      navigate('/');
    }
  }, [isAuthenticated, status, navigate, token]);
  
  // useEffect(() => {
  //   if (status === 'loading') {
  //     dispatch(setStatus({ message: 'Checking session...', variant: 'info' }));
  //   }
  // }, [status, dispatch]);

  return <Outlet />;
}

export default ProtectedURLs;
