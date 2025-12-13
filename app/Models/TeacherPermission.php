<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class TeacherPermission extends Model
{
    /** @use HasFactory<\Database\Factories\TeacherPermissionFactory> */
    use HasFactory;
    protected $fillable = [
        'teacher_id',
        'subject_id',
        'lecture_id',
    ];
    public function teacher()
    {
        return $this->belongsTo(User::class, "teacher_id");
    }

    public function subject()
    {
        return $this->belongsTo(Subject::class);
    }

    public function lecture()
    {
        return $this->belongsTo(Lecture::class);
    }
}
