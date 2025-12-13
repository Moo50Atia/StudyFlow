<x-app-layout>
    <x-slot name="header">
        <div class="flex justify-between items-center">
            <h2 class="font-semibold text-xl text-gray-800 dark:text-gray-200 leading-tight">Question Details</h2>
            <div class="flex items-center space-x-4">
                @auth
                <button onclick="toggleLove('question', {{ $question->id }}, this)" class="love-btn inline-flex items-center px-3 py-2 border rounded-md transition-all duration-200 {{ auth()->user()->loves($question) ? 'border-red-300 text-red-500 bg-red-50' : 'border-gray-300 text-gray-400 hover:bg-gray-50' }}">
                    <svg class="w-5 h-5 mr-1" fill="{{ auth()->user()->loves($question) ? 'currentColor' : 'none' }}" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path>
                    </svg>
                    <span class="text-sm">{{ auth()->user()->loves($question) ? 'Loved' : 'Love' }}</span>
                </button>
                @endauth
                <a href="{{ route('questions.index') }}" class="text-indigo-600 hover:text-indigo-900 dark:text-indigo-400">← Back</a>
            </div>
        </div>
    </x-slot>

    <div class="py-12">
        <div class="max-w-7xl mx-auto sm:px-6 lg:px-8">
            <div class="bg-white dark:bg-gray-800 overflow-hidden shadow-sm sm:rounded-lg animate-fade-in-up">
                <div class="p-6 text-gray-900 dark:text-gray-100">
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                        <div class="animate-fade-in-up" style="animation-delay: 0.1s;">
                            <h3 class="text-sm font-medium text-gray-500">Lecture</h3>
                            <p class="mt-1 text-gray-900 dark:text-gray-100">{{ $question->lecture->title ?? 'N/A' }}</p>
                        </div>
                        <div class="animate-fade-in-up" style="animation-delay: 0.2s;">
                            <h3 class="text-sm font-medium text-gray-500">Subject</h3>
                            <p class="mt-1 text-gray-900 dark:text-gray-100">{{ $question->lecture->subject->name ?? 'N/A' }}</p>
                        </div>
                    </div>

                    @if($question->question_image)
                    <div class="mb-6 animate-fade-in-up" style="animation-delay: 0.3s;">
                        <h3 class="text-lg font-medium text-gray-900 dark:text-gray-100 mb-2">Question Image</h3>
                        <img src="{{ Storage::url($question->question_image) }}" alt="Question" class="max-w-lg rounded-lg shadow-lg">
                    </div>
                    @endif

                    <div class="mb-6 animate-fade-in-up" style="animation-delay: 0.4s;">
                        <h3 class="text-lg font-medium text-gray-900 dark:text-gray-100">Idea/Hint</h3>
                        <p class="mt-1 text-gray-600 dark:text-gray-400">{{ $question->idea_text ?? 'No hint available.' }}</p>
                    </div>

                    @if($question->solution_image)
                    <div class="mb-6 animate-fade-in-up" style="animation-delay: 0.5s;">
                        <h3 class="text-lg font-medium text-gray-900 dark:text-gray-100 mb-2">Solution Image</h3>
                        <img src="{{ Storage::url($question->solution_image) }}" alt="Solution" class="max-w-lg rounded-lg shadow-lg">
                    </div>
                    @endif

                    <div class="mb-6 animate-fade-in-up" style="animation-delay: 0.6s;">
                        <h3 class="text-lg font-medium text-gray-900 dark:text-gray-100">Solution Explanation</h3>
                        <p class="mt-1 text-gray-600 dark:text-gray-400">{{ $question->solution_explanation ?? 'No explanation available.' }}</p>
                    </div>

                    @if(Auth::check() && Auth::user()->role !== 'student')
                    <div class="mt-6 pt-6 border-t dark:border-gray-700 flex space-x-4 animate-fade-in-up" style="animation-delay: 0.7s;">
                        <a href="{{ route('questions.edit', $question) }}" class="inline-flex items-center px-4 py-2 bg-yellow-500 border border-transparent rounded-md font-semibold text-xs text-white uppercase tracking-widest hover:bg-yellow-600 transition ease-in-out duration-150">Edit</a>
                        <form action="{{ route('questions.destroy', $question) }}" method="POST" class="inline">
                            @csrf
                            @method('DELETE')
                            <button type="submit" onclick="return confirm('Are you sure?')" class="inline-flex items-center px-4 py-2 bg-red-600 border border-transparent rounded-md font-semibold text-xs text-white uppercase tracking-widest hover:bg-red-700 transition ease-in-out duration-150">Delete</button>
                        </form>
                    </div>
                    @endif
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
                        const span = button.querySelector('span');
                        if (data.is_loved) {
                            button.classList.remove('border-gray-300', 'text-gray-400', 'hover:bg-gray-50');
                            button.classList.add('border-red-300', 'text-red-500', 'bg-red-50');
                            svg.setAttribute('fill', 'currentColor');
                            span.textContent = 'Loved';
                        } else {
                            button.classList.remove('border-red-300', 'text-red-500', 'bg-red-50');
                            button.classList.add('border-gray-300', 'text-gray-400', 'hover:bg-gray-50');
                            svg.setAttribute('fill', 'none');
                            span.textContent = 'Love';
                        }
                    }
                });
        }
    </script>
    @endauth
</x-app-layout>