<?php

namespace Database\Factories;

use Illuminate\Database\Eloquent\Factories\Factory;

/**
 * @extends \Illuminate\Database\Eloquent\Factories\Factory<\App\Models\Subject>
 */
class SubjectFactory extends Factory
{
    /**
     * Define the model's default state.
     *
     * @return array<string, mixed>
     */
    public function definition(): array
    {
        $subjects = [
            'Mathematics' => 'Comprehensive study of numbers, quantities, and shapes including algebra, calculus, and geometry.',
            'Physics' => 'Study of matter, energy, and the fundamental forces of nature.',
            'Chemistry' => 'Study of substances, their properties, and reactions.',
            'Biology' => 'Study of living organisms and their vital processes.',
            'Computer Science' => 'Study of computation, algorithms, and programming.',
            'English Literature' => 'Study of written works in the English language.',
            'History' => 'Study of past events, civilizations, and human development.',
            'Economics' => 'Study of production, distribution, and consumption of goods.',
        ];

        $name = fake()->unique()->randomElement(array_keys($subjects));

        return [
            'name' => $name,
            'description' => $subjects[$name],
        ];
    }
}
