<x-app-layout>
    <x-slot name="header">
        <div class="flex justify-between items-center">
            <h2 class="font-semibold text-xl text-gray-800 dark:text-gray-200 leading-tight animate-fade-in">
                {{ __('Permission Details') }}
            </h2>
            <a href="{{ route('teacher_permissions.index') }}" class="inline-flex items-center text-indigo-600 hover:text-indigo-800 dark:text-indigo-400 transition-colors duration-200">
                <svg class="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                </svg>
                Back to Permissions
            </a>
        </div>
    </x-slot>

    <div class="py-12">
        <div class="max-w-4xl mx-auto sm:px-6 lg:px-8">
            <div class="bg-white dark:bg-gray-800 overflow-hidden shadow-xl rounded-2xl animate-fade-in-up">
                <div class="p-8">
                    <!-- Teacher Section -->
                    <div class="mb-8 animate-fade-in-up" style="animation-delay: 0.1s">
                        <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4 flex items-center">
                            <span class="w-8 h-8 rounded-lg bg-indigo-100 dark:bg-indigo-900 flex items-center justify-center mr-3">
                                <svg class="w-5 h-5 text-indigo-600 dark:text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                                </svg>
                            </span>
                            Teacher Information
                        </h3>
                        <div class="bg-gray-50 dark:bg-gray-700 rounded-xl p-6">
                            <div class="flex items-center">
                                <div class="w-16 h-16 rounded-full bg-gradient-to-r from-indigo-500 to-purple-500 flex items-center justify-center text-white text-2xl font-bold">
                                    {{ substr($teacherPermission->teacher->name ?? 'N', 0, 1) }}
                                </div>
                                <div class="ml-6">
                                    <p class="text-xl font-semibold text-gray-900 dark:text-gray-100">{{ $teacherPermission->teacher->name ?? 'N/A' }}</p>
                                    <p class="text-gray-500 dark:text-gray-400">{{ $teacherPermission->teacher->email ?? 'N/A' }}</p>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Subject Section -->
                    <div class="mb-8 animate-fade-in-up" style="animation-delay: 0.2s">
                        <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4 flex items-center">
                            <span class="w-8 h-8 rounded-lg bg-blue-100 dark:bg-blue-900 flex items-center justify-center mr-3">
                                <svg class="w-5 h-5 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                                </svg>
                            </span>
                            Subject Access
                        </h3>
                        <div class="bg-gray-50 dark:bg-gray-700 rounded-xl p-6">
                            <span class="px-4 py-2 inline-flex text-sm font-semibold rounded-full bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200">
                                {{ $teacherPermission->subject->name ?? 'N/A' }}
                            </span>
                            <p class="mt-3 text-gray-600 dark:text-gray-400">{{ $teacherPermission->subject->description ?? 'No description available' }}</p>
                        </div>
                    </div>

                    <!-- Lecture Section -->
                    <div class="mb-8 animate-fade-in-up" style="animation-delay: 0.3s">
                        <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4 flex items-center">
                            <span class="w-8 h-8 rounded-lg bg-green-100 dark:bg-green-900 flex items-center justify-center mr-3">
                                <svg class="w-5 h-5 text-green-600 dark:text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                                </svg>
                            </span>
                            Lecture Access
                        </h3>
                        <div class="bg-gray-50 dark:bg-gray-700 rounded-xl p-6">
                            <p class="text-gray-900 dark:text-gray-100 font-medium">{{ $teacherPermission->lecture->title ?? 'All Lectures' }}</p>
                            @if($teacherPermission->lecture)
                            <p class="mt-2 text-gray-600 dark:text-gray-400">{{ $teacherPermission->lecture->summary ?? '' }}</p>
                            @endif
                        </div>
                    </div>

                    <!-- Actions -->
                    <div class="flex space-x-4 animate-fade-in-up" style="animation-delay: 0.4s">
                        <a href="{{ route('teacher_permissions.edit', $teacherPermission) }}" class="inline-flex items-center px-6 py-3 bg-gradient-to-r from-amber-500 to-orange-500 text-white rounded-xl font-semibold hover:from-amber-600 hover:to-orange-600 transition-all duration-300 transform hover:scale-105 shadow-lg">
                            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                            </svg>
                            Edit Permission
                        </a>
                        <form action="{{ route('teacher_permissions.destroy', $teacherPermission) }}" method="POST" class="inline">
                            @csrf
                            @method('DELETE')
                            <button type="submit" onclick="return confirm('Are you sure you want to delete this permission?')" class="inline-flex items-center px-6 py-3 bg-gradient-to-r from-red-500 to-rose-500 text-white rounded-xl font-semibold hover:from-red-600 hover:to-rose-600 transition-all duration-300 transform hover:scale-105 shadow-lg">
                                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                                </svg>
                                Delete Permission
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