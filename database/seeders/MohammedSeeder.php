<?php

namespace Database\Seeders;

use App\Models\User;
use App\Models\Subject;
use App\Models\Lecture;
use App\Models\TeacherPermission;
use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\Hash;

class MohammedSeeder extends Seeder
{
    /**
     * Run the database seeds.
     */
    public function run(): void
    {
        // Admin Account
        $admin = User::updateOrCreate(
            ['email' => 'admin@test.com'],
            [
                'name' => 'Mohammed Admin',
                'email' => 'admin@test.com',
                'password' => Hash::make('Password'),
                'role' => 'admin',
            ]
        );

        // Teacher Account
        $teacher = User::updateOrCreate(
            ['email' => 'teacher@test.com'],
            [
                'name' => 'Mohammed Teacher',
                'email' => 'teacher@test.com',
                'password' => Hash::make('Password'),
                'role' => 'teacher',
            ]
        );

        // Student Account
        $student = User::updateOrCreate(
            ['email' => 'student@test.com'],
            [
                'name' => 'Mohammed Student',
                'email' => 'student@test.com',
                'password' => Hash::make('Password'),
                'role' => 'student',
            ]
        );

        // Create Subjects
        $mathSubject = Subject::updateOrCreate(
            ['name' => 'Mathematics'],
            ['name' => 'Mathematics', 'description' => 'Advanced Mathematics including Calculus and Algebra']
        );

        $physicsSubject = Subject::updateOrCreate(
            ['name' => 'Physics'],
            ['name' => 'Physics', 'description' => 'Classical and Modern Physics']
        );

        $chemistrySubject = Subject::updateOrCreate(
            ['name' => 'Chemistry'],
            ['name' => 'Chemistry', 'description' => 'Organic and Inorganic Chemistry']
        );

        $biologySubject = Subject::updateOrCreate(
            ['name' => 'Biology'],
            ['name' => 'Biology', 'description' => 'Life Sciences and Anatomy']
        );

        $computerSubject = Subject::updateOrCreate(
            ['name' => 'Computer Science'],
            ['name' => 'Computer Science', 'description' => 'Programming and Software Development']
        );

        // Create Lectures for subjects
        $mathLecture = Lecture::updateOrCreate(
            ['title' => 'Introduction to Calculus', 'subject_id' => $mathSubject->id],
            ['title' => 'Introduction to Calculus', 'subject_id' => $mathSubject->id, 'summary' => 'Basic concepts of differential calculus']
        );

        $physicsLecture = Lecture::updateOrCreate(
            ['title' => 'Newtonian Mechanics', 'subject_id' => $physicsSubject->id],
            ['title' => 'Newtonian Mechanics', 'subject_id' => $physicsSubject->id, 'summary' => 'Laws of motion and forces']
        );

        $chemistryLecture = Lecture::updateOrCreate(
            ['title' => 'Organic Compounds', 'subject_id' => $chemistrySubject->id],
            ['title' => 'Organic Compounds', 'subject_id' => $chemistrySubject->id, 'summary' => 'Introduction to organic chemistry']
        );

        $biologyLecture = Lecture::updateOrCreate(
            ['title' => 'Cell Biology', 'subject_id' => $biologySubject->id],
            ['title' => 'Cell Biology', 'subject_id' => $biologySubject->id, 'summary' => 'Structure and function of cells']
        );

        $computerLecture = Lecture::updateOrCreate(
            ['title' => 'Introduction to Programming', 'subject_id' => $computerSubject->id],
            ['title' => 'Introduction to Programming', 'subject_id' => $computerSubject->id, 'summary' => 'Basic programming concepts']
        );

        // Assign Teacher Permissions (only for Mathematics and Physics)
        // Teacher can CRUD on Mathematics and Physics, but only view Chemistry, Biology, Computer Science
        TeacherPermission::updateOrCreate(
            ['teacher_id' => $teacher->id, 'subject_id' => $mathSubject->id],
            [
                'teacher_id' => $teacher->id,
                'subject_id' => $mathSubject->id,
                'lecture_id' => $mathLecture->id,
            ]
        );

        TeacherPermission::updateOrCreate(
            ['teacher_id' => $teacher->id, 'subject_id' => $physicsSubject->id],
            [
                'teacher_id' => $teacher->id,
                'subject_id' => $physicsSubject->id,
                'lecture_id' => $physicsLecture->id,
            ]
        );

        $this->command->info('');
        $this->command->info('✅ Mohammed Seeder completed!');
        $this->command->info('');
        $this->command->info('📧 Test Accounts Created:');
        $this->command->info('┌───────────────────────────────────────────────────┐');
        $this->command->info('│  Role     │  Email              │  Password      │');
        $this->command->info('├───────────────────────────────────────────────────┤');
        $this->command->info('│  Admin    │  admin@test.com     │  password      │');
        $this->command->info('│  Teacher  │  teacher@test.com   │  password      │');
        $this->command->info('│  Student  │  student@test.com   │  password      │');
        $this->command->info('└───────────────────────────────────────────────────┘');
        $this->command->info('');
        $this->command->info('📚 Subjects Created:');
        $this->command->info('  - Mathematics');
        $this->command->info('  - Physics');
        $this->command->info('  - Chemistry');
        $this->command->info('  - Biology');
        $this->command->info('  - Computer Science');
        $this->command->info('');
        $this->command->info('👨‍🏫 Teacher Permissions:');
        $this->command->info('  ✅ Can CRUD: Mathematics, Physics');
        $this->command->info('  👁️ View Only: Chemistry, Biology, Computer Science');
    }
}
