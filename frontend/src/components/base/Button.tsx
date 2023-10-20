import React, { ReactNode } from 'react';
import { Spinner } from './Spinner';

export interface ButtonProps {
  className?: string;
  loading?: boolean;
  children?: ReactNode;
  [key: string]: unknown;
}

export const Button = ({ className, loading, ...props }: ButtonProps) => {
  const defaultClassName =
    'rounded-lg bg-purple-700 box-shadow-xl px-8 py-4 \
    text-white font-bold uppercase hover:bg-purple-800 active:scale-95 \
    flex items-center disabled:bg-slate-500';
  className = className ? ' ' + className : '';
  return (
    <button className={defaultClassName + className} {...props}>
      {props.children && props.children}
      {loading && (
        <div className="ml-2">
          <Spinner />
        </div>
      )}
    </button>
  );
};
