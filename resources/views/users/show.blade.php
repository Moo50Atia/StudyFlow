<x-app-layout>
    <x-slot name="header">
        <div class="flex justify-between items-center">
            <h2 class="font-semibold text-xl text-gray-800 dark:text-gray-200 leading-tight animate-fade-in">User Details</h2>
            <a href="{{ route('users.index') }}" class="inline-flex items-center text-indigo-600 hover:text-indigo-800 dark:text-indigo-400 transition-colors duration-200">
                <svg class="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                </svg>
                Back to Users
            </a>
        </div>
    </x-slot>

    <div class="py-12">
        <div class="max-w-4xl mx-auto sm:px-6 lg:px-8">
            <div class="bg-white dark:bg-gray-800 overflow-hidden shadow-xl rounded-2xl animate-fade-in-up">
                <div class="p-8">
                    <!-- User Profile -->
                    <div class="flex items-center mb-8 animate-fade-in-up" style="animation-delay: 0.1s">
                        <div class="w-24 h-24 rounded-full bg-gradient-to-r {{ $user->role === 'admin' ? 'from-red-500 to-rose-500' : ($user->role === 'teacher' ? 'from-blue-500 to-indigo-500' : 'from-green-500 to-emerald-500') }} flex items-center justify-center text-white text-4xl font-bold shadow-xl">
                            {{ strtoupper(substr($user->name, 0, 1)) }}
                        </div>
                        <div class="ml-6">
                            <h3 class="text-2xl font-bold text-gray-900 dark:text-gray-100">{{ $user->name }}</h3>
                            <p class="text-gray-500 dark:text-gray-400">{{ $user->email }}</p>
                            <div class="mt-2">
                                @if($user->role === 'admin')
                                <span class="px-4 py-1.5 inline-flex text-sm font-semibold rounded-full bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200">👑 Administrator</span>
                                @elseif($user->role === 'teacher')
                                <span class="px-4 py-1.5 inline-flex text-sm font-semibold rounded-full bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200">👨‍🏫 Teacher</span>
                                @else
                                <span class="px-4 py-1.5 inline-flex text-sm font-semibold rounded-full bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200">👨‍🎓 Student</span>
                                @endif
                            </div>
                        </div>
                    </div>

                    @if($user->role === 'teacher' && $user->teacherPermissions->count() > 0)
                    <div class="mb-8 animate-fade-in-up" style="animation-delay: 0.2s">
                        <h4 class="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">Teaching Permissions</h4>
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                            @foreach($user->teacherPermissions as $permission)
                            <div class="bg-gray-50 dark:bg-gray-700 rounded-xl p-4">
                                <p class="font-medium text-gray-900 dark:text-gray-100">{{ $permission->subject->name ?? 'N/A' }}</p>
                                <p class="text-sm text-gray-500 dark:text-gray-400">{{ $permission->lecture->title ?? 'All Lectures' }}</p>
                            </div>
                            @endforeach
                        </div>
                    </div>
                    @endif

                    <div class="flex space-x-4 animate-fade-in-up" style="animation-delay: 0.3s">
                        <a href="{{ route('users.edit', $user) }}" class="inline-flex items-center px-6 py-3 bg-gradient-to-r from-amber-500 to-orange-500 text-white rounded-xl font-semibold hover:from-amber-600 hover:to-orange-600 transition-all duration-300 transform hover:scale-105 shadow-lg">
                            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                            </svg>
                            Edit User
                        </a>
                        <form action="{{ route('users.destroy', $user) }}" method="POST" class="inline">
                            @csrf
                            @method('DELETE')
                            <button type="submit" onclick="return confirm('Are you sure?')" class="inline-flex items-center px-6 py-3 bg-gradient-to-r from-red-500 to-rose-500 text-white rounded-xl font-semibold hover:from-red-600 hover:to-rose-600 transition-all duration-300 transform hover:scale-105 shadow-lg">
                                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                                </svg>
                                Delete User
                            </button>
                        </form>
                    </div>
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