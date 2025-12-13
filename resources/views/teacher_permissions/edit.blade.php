<x-app-layout>
    <x-slot name="header">
        <div class="flex justify-between items-center">
            <h2 class="font-semibold text-xl text-gray-800 dark:text-gray-200 leading-tight animate-fade-in">
                {{ __('Edit Teacher Permission') }}
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
        <div class="max-w-2xl mx-auto sm:px-6 lg:px-8">
            <div class="bg-white dark:bg-gray-800 overflow-hidden shadow-xl rounded-2xl animate-fade-in-up">
                <div class="p-8">
                    <form action="{{ route('teacher_permissions.update', $teacherPermission) }}" method="POST">
                        @csrf
                        @method('PUT')

                        <!-- Teacher Selection -->
                        <div class="mb-6 animate-fade-in-up" style="animation-delay: 0.1s">
                            <label for="teacher_id" class="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
                                <span class="flex items-center">
                                    <svg class="w-5 h-5 mr-2 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                                    </svg>
                                    Select Teacher
                                </span>
                            </label>
                            <select name="teacher_id" id="teacher_id" required class="w-full rounded-xl border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-gray-100 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 transition-all duration-200">
                                <option value="">-- Select a Teacher --</option>
                                @foreach($teachers as $teacher)
                                <option value="{{ $teacher->id }}" {{ (old('teacher_id', $teacherPermission->teacher_id) == $teacher->id) ? 'selected' : '' }}>{{ $teacher->name }} ({{ $teacher->email }})</option>
                                @endforeach
                            </select>
                            @error('teacher_id')
                            <p class="mt-2 text-sm text-red-500">{{ $message }}</p>
                            @enderror
                        </div>

                        <!-- Subject Selection -->
                        <div class="mb-6 animate-fade-in-up" style="animation-delay: 0.2s">
                            <label for="subject_id" class="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
                                <span class="flex items-center">
                                    <svg class="w-5 h-5 mr-2 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                                    </svg>
                                    Select Subject
                                </span>
                            </label>
                            <select name="subject_id" id="subject_id" required class="w-full rounded-xl border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-gray-100 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 transition-all duration-200">
                                <option value="">-- Select a Subject --</option>
                                @foreach($subjects as $subject)
                                <option value="{{ $subject->id }}" {{ (old('subject_id', $teacherPermission->subject_id) == $subject->id) ? 'selected' : '' }}>{{ $subject->name }}</option>
                                @endforeach
                            </select>
                            @error('subject_id')
                            <p class="mt-2 text-sm text-red-500">{{ $message }}</p>
                            @enderror
                        </div>

                        <!-- Lecture Selection (Optional) -->
                        <div class="mb-8 animate-fade-in-up" style="animation-delay: 0.3s">
                            <label for="lecture_id" class="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
                                <span class="flex items-center">
                                    <svg class="w-5 h-5 mr-2 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                                    </svg>
                                    Select Lecture (Optional)
                                </span>
                            </label>
                            <select name="lecture_id" id="lecture_id" class="w-full rounded-xl border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-gray-100 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 transition-all duration-200">
                                <option value="">-- All Lectures in Subject --</option>
                                @foreach($lectures as $lecture)
                                <option value="{{ $lecture->id }}" {{ (old('lecture_id', $teacherPermission->lecture_id) == $lecture->id) ? 'selected' : '' }}>{{ $lecture->title }}</option>
                                @endforeach
                            </select>
                            @error('lecture_id')
                            <p class="mt-2 text-sm text-red-500">{{ $message }}</p>
                            @enderror
                        </div>

                        <!-- Submit Button -->
                        <div class="animate-fade-in-up" style="animation-delay: 0.4s">
                            <button type="submit" class="w-full inline-flex items-center justify-center px-6 py-4 bg-gradient-to-r from-amber-500 to-orange-500 text-white rounded-xl font-bold text-lg hover:from-amber-600 hover:to-orange-600 transition-all duration-300 transform hover:scale-[1.02] shadow-xl">
                                <svg class="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                                </svg>
                                Update Permission
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