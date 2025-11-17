import { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { checkAuthStatus } from '@redux/auth/authSlice';
import { Outlet, useNavigate } from 'react-router-dom';
import { setStatus } from '@redux/status/statusSlice';

function ProtectedURLs() {
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const { isAuthenticated, status } = useSelector((state) => state.auth);

  useEffect(() => {
    dispatch(checkAuthStatus());
  }, [dispatch]);

  useEffect(() => {
    
    if (status === 'failed' || (!isAuthenticated && status !== 'loading')) {
      navigate('/');
      
    }
  }, [isAuthenticated, status, navigate]);
  
  if (status === 'loading') {
    dispatch(setStatus('Checking session...'));
  }

  return <Outlet />;
}

export default ProtectedURLs;
