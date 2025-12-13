<?php

namespace Database\Factories;

use App\Models\Lecture;
use Illuminate\Database\Eloquent\Factories\Factory;

/**
 * @extends \Illuminate\Database\Eloquent\Factories\Factory<\App\Models\Section>
 */
class SectionFactory extends Factory
{
    /**
     * Define the model's default state.
     *
     * @return array<string, mixed>
     */
    public function definition(): array
    {
        $sectionTitles = [
            'Key Definitions',
            'Core Concepts',
            'Step-by-Step Guide',
            'Examples and Exercises',
            'Summary Points',
            'Quick Review',
            'Important Formulas',
            'Practice Problems',
        ];

        return [
            'lecture_id' => Lecture::factory(),
            'title' => fake()->randomElement($sectionTitles),
            'quick_summary' => fake()->sentence(10),
            'notebook_link' => fake()->optional(0.7)->url(),
            'dynamic_view_link' => fake()->optional(0.5)->url(),
        ];
    }
}
