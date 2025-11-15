// Reusable button styles
export const baseBtn = {
  border: '1px solid transparent',
  borderRadius: 6,
  padding: '.5rem .9rem',
  cursor: 'pointer',
  fontWeight: 700,
};

export const primaryBtn = {
  ...baseBtn,
  background: '#4c8bf5',
  borderColor: '#2f6fda',
  color: 'white',
};

export const darkBtn = {
  ...baseBtn,
  background: '#1f2937',
  color: 'white',
};

export const mutedBtn = {
  ...baseBtn,
  background: '#e8eef6',
  color: '#1f2937',
  borderColor: '#c8d3e0',
};
