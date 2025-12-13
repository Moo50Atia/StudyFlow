<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Section extends Model
{
    /** @use HasFactory<\Database\Factories\SectionFactory> */
    use HasFactory;
    protected $fillable = [
        'lecture_id',
        'title',
        'quick_summary',
        'notebook_link',
        'dynamic_view_link',
    ];
    public function lecture()
    {
        return $this->belongsTo(Lecture::class);
    }
}
