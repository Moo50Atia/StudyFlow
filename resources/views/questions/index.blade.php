<x-app-layout>
    <x-slot name="header">
        <div class="flex justify-between items-center">
            <h2 class="font-semibold text-xl text-gray-800 dark:text-gray-200 leading-tight">{{ __('Questions') }}</h2>
            @if(Auth::check() && Auth::user()->role !== 'student')
            <a href="{{ route('questions.create') }}" class="inline-flex items-center px-4 py-2 bg-indigo-600 border border-transparent rounded-md font-semibold text-xs text-white uppercase tracking-widest hover:bg-indigo-700 transition ease-in-out duration-150">Create Question</a>
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
                        @forelse($questions as $index => $question)
                        <div class="border dark:border-gray-700 rounded-xl overflow-hidden hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1 animate-fade-in-up" style="animation-delay: {{ $index * 0.1 }}s;">
                            @if($question->question_image)
                            <img src="{{ Storage::url($question->question_image) }}" alt="Question" class="w-full h-40 object-cover">
                            @else
                            <div class="w-full h-40 bg-gradient-to-r from-blue-400 to-indigo-500 flex items-center justify-center">
                                <span class="text-white text-4xl">❓</span>
                            </div>
                            @endif
                            <div class="p-5">
                                <div class="flex items-start justify-between mb-2">
                                    <span class="inline-block px-2 py-1 text-xs bg-green-100 text-green-800 rounded-full">{{ $question->lecture->title ?? 'N/A' }}</span>
                                    @auth
                                    <button onclick="toggleLove('question', {{ $question->id }}, this)" class="love-btn p-1 rounded-full hover:bg-red-50 dark:hover:bg-gray-700 transition-all duration-200 {{ auth()->user()->loves($question) ? 'text-red-500' : 'text-gray-400' }}">
                                        <svg class="w-5 h-5" fill="{{ auth()->user()->loves($question) ? 'currentColor' : 'none' }}" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path>
                                        </svg>
                                    </button>
                                    @endauth
                                </div>
                                <p class="text-sm text-gray-600 dark:text-gray-400 mb-3">{{ Str::limit($question->idea_text, 80) }}</p>
                                <div class="flex items-center justify-between">
                                    <a href="{{ route('questions.show', $question) }}" class="text-indigo-600 hover:text-indigo-900 text-sm font-medium">View →</a>
                                    @if(Auth::check() && Auth::user()->role !== 'student')
                                    <div class="flex space-x-2">
                                        <a href="{{ route('questions.edit', $question) }}" class="text-yellow-600 hover:text-yellow-800 text-xs">Edit</a>
                                    </div>
                                    @endif
                                </div>
                            </div>
                        </div>
                        @empty
                        <div class="col-span-3 text-center py-12 text-gray-500">No questions found.</div>
                        @endforelse
                    </div>
                    <div class="mt-6">{{ $questions->links() }}</div>
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
                            button.classList.add('text-red-500');
                            svg.setAttribute('fill', 'currentColor');
                        } else {
                            button.classList.remove('text-red-500');
                            button.classList.add('text-gray-400');
                            svg.setAttribute('fill', 'none');
                        }
                    }
                });
        }
    </script>
    @endauth
</x-app-layout>