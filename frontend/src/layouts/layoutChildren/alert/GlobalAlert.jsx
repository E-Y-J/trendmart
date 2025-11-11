import { useSelector } from 'react-redux';
import AlertSpace from './AlertSpace';

function GlobalAlert() {
  const { message, variant } = useSelector((state) => state.status);
  if (!message.length) return null;

  return <AlertSpace alertMessage={ message } variant={ variant } />;
}

export default GlobalAlert;