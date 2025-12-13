<x-app-layout>
    <x-slot name="header">
        <div class="flex justify-between items-center">
            <h2 class="font-semibold text-xl text-gray-800 dark:text-gray-200 leading-tight animate-fade-in">{{ $subject->name }}</h2>
            <a href="{{ route('subjects.index') }}" class="inline-flex items-center text-indigo-600 hover:text-indigo-800 dark:text-indigo-400 transition-colors duration-200">
                <svg class="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                </svg>
                Back to Subjects
            </a>
        </div>
    </x-slot>

    <div class="py-12">
        <div class="max-w-7xl mx-auto sm:px-6 lg:px-8">
            <div class="bg-white dark:bg-gray-800 overflow-hidden shadow-xl rounded-2xl animate-fade-in-up">
                <div class="p-8">
                    <div class="mb-8 animate-fade-in-up" style="animation-delay: 0.1s">
                        <div class="flex items-center mb-4">
                            <div class="w-16 h-16 rounded-xl bg-gradient-to-r from-blue-500 to-indigo-500 flex items-center justify-center text-white text-3xl shadow-lg">
                                📚
                            </div>
                            <div class="ml-6">
                                <h3 class="text-2xl font-bold text-gray-900 dark:text-gray-100">{{ $subject->name }}</h3>
                                <p class="text-gray-500 dark:text-gray-400">{{ $subject->lectures->count() }} Lectures</p>
                            </div>
                        </div>
                        <p class="text-gray-600 dark:text-gray-400 mt-4">{{ $subject->description ?? 'No description available' }}</p>
                    </div>

                    @if($subject->lectures->count() > 0)
                    <div class="mb-8 animate-fade-in-up" style="animation-delay: 0.2s">
                        <h4 class="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">Related Lectures</h4>
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                            @foreach($subject->lectures as $lecture)
                            <a href="{{ route('lectures.show', $lecture) }}" class="bg-gray-50 dark:bg-gray-700 rounded-xl p-4 hover:shadow-lg transition-all duration-200 hover:-translate-y-0.5">
                                <p class="font-medium text-gray-900 dark:text-gray-100">{{ $lecture->title }}</p>
                                <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">{{ Str::limit($lecture->summary, 60) }}</p>
                            </a>
                            @endforeach
                        </div>
                    </div>
                    @endif

                    @if(Auth::check() && Auth::user()->role !== 'student')
                    <div class="flex space-x-4 animate-fade-in-up" style="animation-delay: 0.3s">
                        <a href="{{ route('subjects.edit', $subject) }}" class="inline-flex items-center px-6 py-3 bg-gradient-to-r from-amber-500 to-orange-500 text-white rounded-xl font-semibold hover:from-amber-600 hover:to-orange-600 transition-all duration-300 transform hover:scale-105 shadow-lg">
                            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                            </svg>
                            Edit
                        </a>
                        <form action="{{ route('subjects.destroy', $subject) }}" method="POST" class="inline">
                            @csrf
                            @method('DELETE')
                            <button type="submit" onclick="return confirm('Are you sure?')" class="inline-flex items-center px-6 py-3 bg-gradient-to-r from-red-500 to-rose-500 text-white rounded-xl font-semibold hover:from-red-600 hover:to-rose-600 transition-all duration-300 transform hover:scale-105 shadow-lg">
                                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                                </svg>
                                Delete
                            </button>
                        </form>
                    </div>
                    @endif
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