<x-app-layout>
    <x-slot name="header">
        <div class="flex justify-between items-center">
            <h2 class="font-semibold text-xl text-gray-800 dark:text-gray-200 leading-tight">{{ __('Lectures') }}</h2>
            @if(Auth::check() && Auth::user()->role !== 'student')
            <a href="{{ route('lectures.create') }}" class="inline-flex items-center px-4 py-2 bg-indigo-600 border border-transparent rounded-md font-semibold text-xs text-white uppercase tracking-widest hover:bg-indigo-700 transition ease-in-out duration-150">Create Lecture</a>
            @endif
        </div>
    </x-slot>

    <div class="py-12">
        <div class="max-w-7xl mx-auto sm:px-6 lg:px-8">
            @if(session('success'))
            <div class="mb-4 bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded relative animate-fade-in">{{ session('success') }}</div>
            @endif

            <div class="bg-white dark:bg-gray-800 overflow-hidden shadow-sm sm:rounded-lg">
                <div class="p-6 text-gray-900 dark:text-gray-100">
                    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        @forelse($lectures as $index => $lecture)
                        <div class="border dark:border-gray-700 rounded-xl overflow-hidden hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1 animate-fade-in-up" style="animation-delay: {{ $index * 0.1 }}s;">
                            <div class="p-5">
                                <div class="flex items-start justify-between">
                                    <div class="flex-1">
                                        <span class="inline-block px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded-full mb-2">{{ $lecture->subject->name ?? 'N/A' }}</span>
                                        <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100">{{ $lecture->title }}</h3>
                                    </div>
                                    @auth
                                    <button onclick="toggleLove('lecture', {{ $lecture->id }}, this)" class="love-btn p-2 rounded-full hover:bg-red-50 dark:hover:bg-gray-700 transition-all duration-200 {{ auth()->user()->loves($lecture) ? 'text-red-500' : 'text-gray-400' }}">
                                        <svg class="w-6 h-6 transform transition-transform duration-200 hover:scale-110" fill="{{ auth()->user()->loves($lecture) ? 'currentColor' : 'none' }}" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path>
                                        </svg>
                                    </button>
                                    @endauth
                                </div>
                                <p class="text-sm text-gray-500 dark:text-gray-400 mt-2">{{ Str::limit($lecture->summary, 80) }}</p>

                                @if($lecture->pdf_path)
                                <div class="mt-3">
                                    <a href="{{ Storage::url($lecture->pdf_path) }}" target="_blank" class="inline-flex items-center text-sm text-indigo-600 hover:text-indigo-800">
                                        <svg class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                                            <path fill-rule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4z" clip-rule="evenodd"></path>
                                        </svg>
                                        View PDF
                                    </a>
                                </div>
                                @endif

                                <div class="mt-4 pt-4 border-t dark:border-gray-700 flex items-center justify-between">
                                    <a href="{{ route('lectures.show', $lecture) }}" class="text-indigo-600 hover:text-indigo-900 dark:text-indigo-400 text-sm font-medium">View Details →</a>
                                    @if(Auth::check() && Auth::user()->role !== 'student')
                                    <div class="flex space-x-2">
                                        <a href="{{ route('lectures.edit', $lecture) }}" class="text-yellow-600 hover:text-yellow-800 text-sm">Edit</a>
                                        <form action="{{ route('lectures.destroy', $lecture) }}" method="POST" class="inline">
                                            @csrf
                                            @method('DELETE')
                                            <button type="submit" onclick="return confirm('Are you sure?')" class="text-red-600 hover:text-red-800 text-sm">Delete</button>
                                        </form>
                                    </div>
                                    @endif
                                </div>
                            </div>
                        </div>
                        @empty
                        <div class="col-span-3 text-center py-12 text-gray-500 dark:text-gray-400">
                            <svg class="w-16 h-16 mx-auto mb-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>
                            </svg>
                            No lectures found.
                        </div>
                        @endforelse
                    </div>

                    <div class="mt-6">{{ $lectures->links() }}</div>
                </div>
            </div>
        </div>
    </div>

    <style>
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

        .animate-fade-in-up {
            animation: fadeInUp 0.5s ease-out forwards;
            opacity: 0;
        }

        @keyframes fadeIn {
            from {
                opacity: 0;
            }

            to {
                opacity: 1;
            }
        }

        .animate-fade-in {
            animation: fadeIn 0.3s ease-out;
        }

        @keyframes heartBeat {

            0%,
            100% {
                transform: scale(1);
            }

            50% {
                transform: scale(1.3);
            }
        }

        .love-btn.loved svg {
            animation: heartBeat 0.4s ease-in-out;
        }
    </style>

    @auth
    <script>
        function toggleLove(type, id, button) {
            fetch('{{ route("love.toggle") }}', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRF-TOKEN': '{{ csrf_token() }}'
                    },
                    body: JSON.stringify({
                        type: type,
                        id: id
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        const svg = button.querySelector('svg');
                        if (data.is_loved) {
                            button.classList.remove('text-gray-400');
                            button.classList.add('text-red-500', 'loved');
                            svg.setAttribute('fill', 'currentColor');
                        } else {
                            button.classList.remove('text-red-500', 'loved');
                            button.classList.add('text-gray-400');
                            svg.setAttribute('fill', 'none');
                        }
                    }
                });
        }
    </script>
    @endauth
</x-app-layout>