<?php

namespace Database\Factories;

use App\Models\User;
use App\Models\Subject;
use App\Models\Lecture;
use Illuminate\Database\Eloquent\Factories\Factory;

/**
 * @extends \Illuminate\Database\Eloquent\Factories\Factory<\App\Models\TeacherPermission>
 */
class TeacherPermissionFactory extends Factory
{
    /**
     * Define the model's default state.
     *
     * @return array<string, mixed>
     */
    public function definition(): array
    {
        return [
            'teacher_id' => User::factory()->teacher(),
            'subject_id' => Subject::factory(),
            'lecture_id' => Lecture::factory(),
        ];
    }
}
