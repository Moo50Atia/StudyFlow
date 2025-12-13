<x-app-layout>
    <x-slot name="header">
        <div class="flex justify-between items-center">
            <h2 class="font-semibold text-xl text-gray-800 dark:text-gray-200 leading-tight animate-fade-in">Create User</h2>
            <a href="{{ route('users.index') }}" class="inline-flex items-center text-indigo-600 hover:text-indigo-800 dark:text-indigo-400 transition-colors duration-200">
                <svg class="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                </svg>
                Back to Users
            </a>
        </div>
    </x-slot>

    <div class="py-12">
        <div class="max-w-2xl mx-auto sm:px-6 lg:px-8">
            <div class="bg-white dark:bg-gray-800 overflow-hidden shadow-xl rounded-2xl animate-fade-in-up">
                <div class="p-8">
                    <form action="{{ route('users.store') }}" method="POST">
                        @csrf

                        <div class="mb-6 animate-fade-in-up" style="animation-delay: 0.1s">
                            <label for="name" class="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">Name</label>
                            <input type="text" name="name" id="name" value="{{ old('name') }}" required class="w-full rounded-xl border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-gray-100 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 transition-all duration-200">
                            @error('name')<p class="mt-2 text-sm text-red-500">{{ $message }}</p>@enderror
                        </div>

                        <div class="mb-6 animate-fade-in-up" style="animation-delay: 0.2s">
                            <label for="email" class="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">Email</label>
                            <input type="email" name="email" id="email" value="{{ old('email') }}" required class="w-full rounded-xl border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-gray-100 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 transition-all duration-200">
                            @error('email')<p class="mt-2 text-sm text-red-500">{{ $message }}</p>@enderror
                        </div>

                        <div class="mb-6 animate-fade-in-up" style="animation-delay: 0.3s">
                            <label for="password" class="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">Password</label>
                            <input type="password" name="password" id="password" required class="w-full rounded-xl border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-gray-100 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 transition-all duration-200">
                            @error('password')<p class="mt-2 text-sm text-red-500">{{ $message }}</p>@enderror
                        </div>

                        <div class="mb-8 animate-fade-in-up" style="animation-delay: 0.4s">
                            <label for="role" class="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">Role</label>
                            <select name="role" id="role" required class="w-full rounded-xl border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-gray-100 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 transition-all duration-200">
                                <option value="student" {{ old('role') === 'student' ? 'selected' : '' }}>👨‍🎓 Student</option>
                                <option value="teacher" {{ old('role') === 'teacher' ? 'selected' : '' }}>👨‍🏫 Teacher</option>
                                <option value="admin" {{ old('role') === 'admin' ? 'selected' : '' }}>👑 Admin</option>
                            </select>
                            @error('role')<p class="mt-2 text-sm text-red-500">{{ $message }}</p>@enderror
                        </div>

                        <div class="animate-fade-in-up" style="animation-delay: 0.5s">
                            <button type="submit" class="w-full inline-flex items-center justify-center px-6 py-4 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-xl font-bold text-lg hover:from-indigo-700 hover:to-purple-700 transition-all duration-300 transform hover:scale-[1.02] shadow-xl">
                                <svg class="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
                                </svg>
                                Create User
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>

    <style>
        @keyframes fadeIn {
            from {
                opacity: 0;
            }

            to {
                opacity: 1;
            }
        }

        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }

            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .animate-fade-in {
            animation: fadeIn 0.5s ease-out forwards;
        }

        .animate-fade-in-up {
            animation: fadeInUp 0.5s ease-out forwards;
            opacity: 0;
        }
    </style>
</x-app-layout>