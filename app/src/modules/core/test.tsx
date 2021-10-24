import { render, screen } from '@testing-library/react';
import Core from './index';
import Providers from '../../providers';

test('renders learn react link', () => {
    render(
        <Providers>
            <Core />
        </Providers>
    );
    const linkElement = screen.getByText(/NAVBAR/i);
    expect(linkElement).toBeInTheDocument();
});
