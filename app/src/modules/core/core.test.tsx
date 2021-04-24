import React from 'react';
import { render, screen } from '@testing-library/react';
import Core from './index';

test('renders learn react link', () => {
    render(<Core />);
    const linkElement = screen.getByText(/Munity/i);
    expect(linkElement).toBeInTheDocument();
});
