<x-app-layout>
    <x-slot name="header">
        <div class="flex justify-between items-center">
            <h2 class="font-semibold text-xl text-gray-800 dark:text-gray-200 leading-tight animate-fade-in">{{ __('Create Lecture') }}</h2>
            <a href="{{ route('lectures.index') }}" class="inline-flex items-center text-indigo-600 hover:text-indigo-800 dark:text-indigo-400 transition-colors duration-200">
                <svg class="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                </svg>
                Back to Lectures
            </a>
        </div>
    </x-slot>

    <div class="py-12">
        <div class="max-w-2xl mx-auto sm:px-6 lg:px-8">
            <div class="bg-white dark:bg-gray-800 overflow-hidden shadow-xl rounded-2xl animate-fade-in-up">
                <div class="p-8">
                    <form action="{{ route('lectures.store') }}" method="POST" enctype="multipart/form-data">
                        @csrf

                        <div class="mb-6 animate-fade-in-up" style="animation-delay: 0.1s">
                            <label for="subject_id" class="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">Subject *</label>
                            <select name="subject_id" id="subject_id" required class="w-full rounded-xl border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-gray-100 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 transition-all duration-200">
                                <option value="">-- Select a subject --</option>
                                @foreach($subjects as $subject)
                                <option value="{{ $subject->id }}" {{ old('subject_id') == $subject->id ? 'selected' : '' }}>{{ $subject->name }}</option>
                                @endforeach
                            </select>
                            @error('subject_id')<p class="mt-2 text-sm text-red-500">{{ $message }}</p>@enderror
                        </div>

                        <div class="mb-6 animate-fade-in-up" style="animation-delay: 0.2s">
                            <label for="title" class="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">Title *</label>
                            <input type="text" name="title" id="title" value="{{ old('title') }}" required class="w-full rounded-xl border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-gray-100 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 transition-all duration-200">
                            @error('title')<p class="mt-2 text-sm text-red-500">{{ $message }}</p>@enderror
                        </div>

                        <div class="mb-6 animate-fade-in-up" style="animation-delay: 0.3s">
                            <label for="pdf_path" class="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">PDF Document</label>
                            <div class="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 dark:border-gray-600 border-dashed rounded-xl hover:border-indigo-500 transition-colors duration-200">
                                <div class="space-y-1 text-center">
                                    <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
                                    </svg>
                                    <div class="flex text-sm text-gray-600 dark:text-gray-400">
                                        <label for="pdf_path" class="relative cursor-pointer rounded-md font-medium text-indigo-600 hover:text-indigo-500">
                                            <span>Upload PDF</span>
                                            <input id="pdf_path" name="pdf_path" type="file" accept=".pdf" class="sr-only">
                                        </label>
                                    </div>
                                </div>
                            </div>
                            @error('pdf_path')<p class="mt-2 text-sm text-red-500">{{ $message }}</p>@enderror
                        </div>

                        <div class="mb-8 animate-fade-in-up" style="animation-delay: 0.4s">
                            <label for="summary" class="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">Summary</label>
                            <textarea name="summary" id="summary" rows="4" class="w-full rounded-xl border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-gray-100 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 transition-all duration-200">{{ old('summary') }}</textarea>
                            @error('summary')<p class="mt-2 text-sm text-red-500">{{ $message }}</p>@enderror
                        </div>

                        <div class="animate-fade-in-up" style="animation-delay: 0.5s">
                            <button type="submit" class="w-full inline-flex items-center justify-center px-6 py-4 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-xl font-bold text-lg hover:from-indigo-700 hover:to-purple-700 transition-all duration-300 transform hover:scale-[1.02] shadow-xl">
                                <svg class="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                                </svg>
                                Create Lecture
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