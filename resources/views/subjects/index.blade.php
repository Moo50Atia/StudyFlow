<x-app-layout>
    <x-slot name="header">
        <div class="flex justify-between items-center">
            <h2 class="font-semibold text-xl text-gray-800 dark:text-gray-200 leading-tight animate-fade-in">{{ __('Subjects') }}</h2>
            @if(Auth::check() && Auth::user()->role !== 'student')
            <a href="{{ route('subjects.create') }}" class="inline-flex items-center px-4 py-2 bg-gradient-to-r from-indigo-600 to-purple-600 border border-transparent rounded-lg font-semibold text-xs text-white uppercase tracking-widest hover:from-indigo-700 hover:to-purple-700 transition-all duration-300 transform hover:scale-105 shadow-lg">
                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                </svg>
                Create Subject
            </a>
            @endif
        </div>
    </x-slot>

    <div class="py-12">
        <div class="max-w-7xl mx-auto sm:px-6 lg:px-8">
            @if(session('success'))
            <div class="mb-6 bg-gradient-to-r from-green-400 to-emerald-500 text-white px-6 py-4 rounded-xl shadow-lg animate-fade-in-down flex items-center">
                <svg class="w-6 h-6 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                {{ session('success') }}
            </div>
            @endif

            <div class="bg-white dark:bg-gray-800 overflow-hidden shadow-xl rounded-2xl animate-fade-in-up">
                <div class="p-6">
                    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        @forelse($subjects as $index => $subject)
                        <div class="bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-700 dark:to-gray-600 rounded-xl p-6 hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1 animate-fade-in-up" style="animation-delay: {{ $index * 0.05 }}s">
                            <div class="flex items-center mb-4">
                                <div class="w-12 h-12 rounded-xl bg-gradient-to-r from-blue-500 to-indigo-500 flex items-center justify-center text-white text-xl font-bold shadow-lg">
                                    📚
                                </div>
                                <h3 class="ml-4 text-lg font-bold text-gray-900 dark:text-gray-100">{{ $subject->name }}</h3>
                            </div>
                            <p class="text-sm text-gray-600 dark:text-gray-400 mb-4">{{ Str::limit($subject->description, 80) }}</p>
                            <div class="flex space-x-2">
                                <a href="{{ route('subjects.show', $subject) }}" class="flex-1 inline-flex items-center justify-center px-3 py-2 bg-indigo-100 text-indigo-700 rounded-lg hover:bg-indigo-200 transition-colors duration-200 text-sm font-medium">View</a>
                                @if(Auth::check() && Auth::user()->role !== 'student')
                                <a href="{{ route('subjects.edit', $subject) }}" class="flex-1 inline-flex items-center justify-center px-3 py-2 bg-amber-100 text-amber-700 rounded-lg hover:bg-amber-200 transition-colors duration-200 text-sm font-medium">Edit</a>
                                <form action="{{ route('subjects.destroy', $subject) }}" method="POST" class="flex-1">
                                    @csrf
                                    @method('DELETE')
                                    <button type="submit" onclick="return confirm('Are you sure?')" class="w-full inline-flex items-center justify-center px-3 py-2 bg-red-100 text-red-700 rounded-lg hover:bg-red-200 transition-colors duration-200 text-sm font-medium">Delete</button>
                                </form>
                                @endif
                            </div>
                        </div>
                        @empty
                        <div class="col-span-3 text-center py-12">
                            <svg class="w-16 h-16 mx-auto mb-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                            </svg>
                            <p class="text-lg font-medium text-gray-400">No subjects found</p>
                        </div>
                        @endforelse
                    </div>
                    <div class="mt-6">{{ $subjects->links() }}</div>
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

        @keyframes fadeInDown {
            from {
                opacity: 0;
                transform: translateY(-20px);
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

        .animate-fade-in-down {
            animation: fadeInDown 0.5s ease-out forwards;
        }
    </style>
</x-app-layout>