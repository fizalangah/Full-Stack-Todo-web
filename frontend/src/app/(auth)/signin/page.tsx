'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useAuth } from '@/lib/auth';
import { api } from '@/lib/api';

export default function SignInPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const { login } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    try {
      const res = await api.fetch('/api/auth/login', {
        method: 'POST',
        body: JSON.stringify({ email, password }),
      });

      if (res.ok) {
        const data = await res.json();
        // data contains access_token and user from FastAPI
        // We use Better Auth's login flow to handle the token
        login(data.access_token, data.user);
      } else {
        const err = await res.json();
        setError(err.detail || 'Failed to sign in');
      }
    } catch (e) {
      console.error(e);
      setError('An error occurred');
    }
  };

  return (
    <div className="glass-panel p-8 sm:p-12 rounded-3xl shadow-2xl border border-slate-200/80 relative overflow-hidden animate-scale-in">
      {/* Decorative ambient glows */}
      <div className="absolute -top-24 -right-24 w-48 h-48 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none animate-pulse"></div>
      <div className="absolute -bottom-24 -left-24 w-48 h-48 bg-green-500/10 rounded-full blur-3xl pointer-events-none animate-pulse" style={{ animationDelay: '1s' }}></div>

      <div className="relative z-10">
        <div className="flex justify-center mb-6">
          <div className="bg-gradient-to-br from-emerald-500 to-green-600 p-3 rounded-2xl shadow-lg shadow-emerald-500/20">
            <svg className="h-8 w-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
            </svg>
          </div>
        </div>
        <h2 className="text-center text-2xl sm:text-3xl font-black text-slate-800 tracking-tight mb-2">
          Welcome Back
        </h2>
        <p className="text-center text-slate-500 text-sm mb-8 font-medium">
          Enter your details to access your workspace
        </p>
      </div>

      <form className="space-y-6 relative z-10" onSubmit={handleSubmit}>
        {error && (
            <div className="rounded-xl bg-rose-500/10 p-4 border border-rose-500/20 flex items-center animate-fade-in">
              <svg className="h-5 w-5 text-rose-500 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <h3 className="text-sm font-bold text-rose-600">
                  {error}
              </h3>
            </div>
        )}
        
        <div className="space-y-6">
          <div className="group">
            <label htmlFor="email-address" className="block text-xs font-bold text-slate-500 mb-2 uppercase tracking-widest group-hover:text-slate-800 transition-colors">
              Email address
            </label>
            <input
              id="email-address"
              name="email"
              type="email"
              autoComplete="email"
              required
              className="block w-full bg-slate-100/80 backdrop-blur-md border border-slate-200/80 rounded-xl p-4 text-slate-800 placeholder-slate-400 focus:ring-2 focus:ring-emerald-500/50 focus:border-emerald-500 transition-all outline-none group-hover:border-slate-300"
              placeholder="you@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>
          <div className="group">
            <label htmlFor="password" className="block text-xs font-bold text-slate-500 mb-2 uppercase tracking-widest group-hover:text-slate-800 transition-colors">
              Password
            </label>
            <input
              id="password"
              name="password"
              type="password"
              autoComplete="current-password"
              required
              className="block w-full bg-slate-100/80 backdrop-blur-md border border-slate-200/80 rounded-xl p-4 text-slate-800 placeholder-slate-400 focus:ring-2 focus:ring-emerald-500/50 focus:border-emerald-500 transition-all outline-none group-hover:border-slate-300"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>
        </div>

        <div>
          <button
            type="submit"
            className="group relative w-full flex justify-center py-3.5 px-4 border border-transparent text-sm font-bold rounded-xl text-white bg-gradient-to-r from-emerald-600 via-green-600 to-teal-700 hover:from-emerald-700 hover:via-green-700 hover:to-teal-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-emerald-500 transition-all duration-300 shadow-lg shadow-emerald-500/25 hover:shadow-emerald-500/40 hover:-translate-y-0.5 active:scale-95"
          >
            Sign in
          </button>
        </div>
      </form>
      <div className="text-sm text-center mt-8 relative z-10">
        <span className="text-slate-500">Don't have an account? </span>
        <Link href="/signup" className="font-bold text-emerald-600 hover:text-emerald-700 transition-colors border-b border-transparent hover:border-emerald-700 pb-0.5">
          Sign up now
        </Link>
      </div>
    </div>
  );
}
