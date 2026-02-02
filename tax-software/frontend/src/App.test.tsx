import { render, screen } from '@testing-library/react';
import React from 'react';
import App from './App';

test('renders app heading', () => {
  render(<App />);
  expect(screen.getByText(/eROS Tax Preparation Platform/i)).toBeInTheDocument();
});
