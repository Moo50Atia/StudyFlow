<x-app-layout>
    <x-slot name="header">
        <div class="flex justify-between items-center">
            <h2 class="font-semibold text-xl text-gray-800 dark:text-gray-200 leading-tight animate-fade-in">Create Section</h2>
            <a href="{{ route('sections.index') }}" class="inline-flex items-center text-indigo-600 hover:text-indigo-800 dark:text-indigo-400 transition-colors duration-200">
                <svg class="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                </svg>
                Back to Sections
            </a>
        </div>
    </x-slot>

    <div class="py-12">
        <div class="max-w-2xl mx-auto sm:px-6 lg:px-8">
            <div class="bg-white dark:bg-gray-800 overflow-hidden shadow-xl rounded-2xl animate-fade-in-up">
                <div class="p-8">
                    <form action="{{ route('sections.store') }}" method="POST">
                        @csrf

                        <div class="mb-6 animate-fade-in-up" style="animation-delay: 0.1s">
                            <label for="lecture_id" class="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">Lecture</label>
                            <select name="lecture_id" id="lecture_id" required class="w-full rounded-xl border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-gray-100 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 transition-all duration-200">
                                <option value="">-- Select Lecture --</option>
                                @foreach($lectures as $lecture)
                                <option value="{{ $lecture->id }}" {{ old('lecture_id') == $lecture->id ? 'selected' : '' }}>{{ $lecture->title }}</option>
                                @endforeach
                            </select>
                            @error('lecture_id')<p class="mt-2 text-sm text-red-500">{{ $message }}</p>@enderror
                        </div>

                        <div class="mb-6 animate-fade-in-up" style="animation-delay: 0.2s">
                            <label for="title" class="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">Section Title</label>
                            <input type="text" name="title" id="title" value="{{ old('title') }}" required class="w-full rounded-xl border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-gray-100 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 transition-all duration-200">
                            @error('title')<p class="mt-2 text-sm text-red-500">{{ $message }}</p>@enderror
                        </div>

                        <div class="mb-6 animate-fade-in-up" style="animation-delay: 0.3s">
                            <label for="quick_summary" class="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">Quick Summary</label>
                            <textarea name="quick_summary" id="quick_summary" rows="4" class="w-full rounded-xl border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-gray-100 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 transition-all duration-200">{{ old('quick_summary') }}</textarea>
                            @error('quick_summary')<p class="mt-2 text-sm text-red-500">{{ $message }}</p>@enderror
                        </div>

                        <div class="mb-6 animate-fade-in-up" style="animation-delay: 0.4s">
                            <label for="notebook_link" class="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">Notebook Link</label>
                            <input type="url" name="notebook_link" id="notebook_link" value="{{ old('notebook_link') }}" class="w-full rounded-xl border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-gray-100 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 transition-all duration-200">
                            @error('notebook_link')<p class="mt-2 text-sm text-red-500">{{ $message }}</p>@enderror
                        </div>

                        <div class="mb-8 animate-fade-in-up" style="animation-delay: 0.5s">
                            <label for="dynamic_view_link" class="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">Dynamic View Link</label>
                            <input type="url" name="dynamic_view_link" id="dynamic_view_link" value="{{ old('dynamic_view_link') }}" class="w-full rounded-xl border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-gray-100 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 transition-all duration-200">
                            @error('dynamic_view_link')<p class="mt-2 text-sm text-red-500">{{ $message }}</p>@enderror
                        </div>

                        <div class="animate-fade-in-up" style="animation-delay: 0.6s">
                            <button type="submit" class="w-full inline-flex items-center justify-center px-6 py-4 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-xl font-bold text-lg hover:from-indigo-700 hover:to-purple-700 transition-all duration-300 transform hover:scale-[1.02] shadow-xl">
                                <svg class="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                                </svg>
                                Create Section
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