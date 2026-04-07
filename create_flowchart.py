import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.patheffects as pe

fig, ax = plt.subplots(figsize=(22, 32))
ax.set_xlim(0, 22)
ax.set_ylim(0, 32)
ax.axis('off')
fig.patch.set_facecolor('#f0f4f8')

C = {
    'start':    '#1e3a5f',
    'auth':     '#0f766e',
    'decision': '#b45309',
    'student':  '#1d4ed8',
    'admin':    '#7c3aed',
    'process':  '#0369a1',
    'output':   '#065f46',
    'end':      '#991b1b',
    'db':       '#334155',
    'security': '#4b5563',
}

ARROW_KW = dict(
    arrowstyle='-|>',
    mutation_scale=18,
    lw=2.0,
    joinstyle='miter',
    capstyle='butt',
)

def draw_box(x, y, w, h, label, color, fontsize=9, sublabel=None, shape='rect'):
    if shape == 'diamond':
        cx, cy = x + w / 2, y + h / 2
        dx, dy = w / 2, h / 2
        pts = [[cx, cy + dy], [cx + dx, cy], [cx, cy - dy], [cx - dx, cy]]
        patch = plt.Polygon(pts, closed=True, facecolor=color,
                            edgecolor='white', linewidth=2, zorder=3)
        ax.add_patch(patch)
        ax.text(cx, cy, label, ha='center', va='center', fontsize=fontsize,
                color='white', fontweight='bold', zorder=4, multialignment='center')
    else:
        style = 'round,pad=0.12' if shape == 'rounded' else 'round,pad=0.06'
        patch = FancyBboxPatch((x, y), w, h, boxstyle=style,
                               facecolor=color, edgecolor='white', linewidth=2, zorder=3)
        ax.add_patch(patch)
        ty = y + h / 2 + (0.18 if sublabel else 0)
        ax.text(x + w / 2, ty, label, ha='center', va='center',
                fontsize=fontsize, color='white', fontweight='bold',
                zorder=4, multialignment='center')
        if sublabel:
            ax.text(x + w / 2, y + h / 2 - 0.22, sublabel,
                    ha='center', va='center', fontsize=7.2,
                    color='#d1fae5', zorder=4, multialignment='center')

def straight_arrow(x1, y1, x2, y2, color='#1e293b', label='', label_side='right'):
    arr = FancyArrowPatch((x1, y1), (x2, y2),
                          connectionstyle='arc3,rad=0.0',
                          color=color, zorder=2, **ARROW_KW)
    ax.add_patch(arr)
    if label:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        ox = 0.18 if label_side == 'right' else -0.18
        ax.text(mx + ox, my, label, fontsize=8, color=color,
                fontweight='bold', va='center', zorder=5)

def elbow_arrow(x1, y1, x2, y2, color='#1e293b', via='h-v', label='', label_pos=0.5):
    """
    via='h-v': go horizontal first then vertical
    via='v-h': go vertical first then horizontal
    """
    if via == 'h-v':
        mid = [(x2, y1), (x2, y2)]
        path_pts = [(x1, y1), (x2, y1), (x2, y2)]
    else:
        path_pts = [(x1, y1), (x1, y2), (x2, y2)]

    xs = [p[0] for p in path_pts]
    ys = [p[1] for p in path_pts]
    ax.plot(xs[:-1], ys[:-1], color=color, lw=2.0, zorder=2, solid_capstyle='round')
    arr = FancyArrowPatch((xs[-2], ys[-2]), (xs[-1], ys[-1]),
                          connectionstyle='arc3,rad=0.0',
                          color=color, zorder=2, **ARROW_KW)
    ax.add_patch(arr)
    if label:
        idx = max(1, int(len(xs) * label_pos))
        lx = (xs[0] + xs[1]) / 2
        ly = (ys[0] + ys[1]) / 2
        ax.text(lx, ly + 0.12, label, fontsize=8, color=color,
                fontweight='bold', ha='center', zorder=5)

# ─────────────────────────────────────────────────────────────────────────────
# TITLE
# ─────────────────────────────────────────────────────────────────────────────
ax.text(11, 31.3, 'Student Recommendation System — Flowchart',
        ha='center', va='center', fontsize=20, fontweight='bold', color='#1e3a5f',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='#dbeafe',
                  edgecolor='#1e3a5f', lw=2.5))
ax.text(11, 30.7, 'Django Backend  |  Full-Stack Web Application',
        ha='center', fontsize=10.5, color='#475569')

# ─────────────────────────────────────────────────────────────────────────────
# START
# ─────────────────────────────────────────────────────────────────────────────
draw_box(9, 29.8, 4, 0.7, 'START', C['start'], fontsize=13, shape='rounded')
straight_arrow(11, 29.8, 11, 29.1)

# ─────────────────────────────────────────────────────────────────────────────
# VISIT WEBSITE
# ─────────────────────────────────────────────────────────────────────────────
draw_box(8, 28.4, 6, 0.65, 'User Visits Website', C['process'],
         sublabel='Home Page / Login Page')
straight_arrow(11, 28.4, 11, 27.7)

# ─────────────────────────────────────────────────────────────────────────────
# HAS ACCOUNT?
# ─────────────────────────────────────────────────────────────────────────────
draw_box(8.2, 26.7, 5.6, 0.9, 'Has Account?', C['decision'], shape='diamond')
straight_arrow(11, 28.4, 11, 27.6)

# NO → Register (left)
elbow_arrow(8.2, 27.15, 5.2, 27.15, color=C['auth'], via='h-v', label='No')
draw_box(3.2, 26.5, 2.8, 0.75, 'Register\nUsername / Email\n/ Password', C['auth'], fontsize=8)
straight_arrow(4.6, 26.5, 4.6, 25.8)
draw_box(3.2, 25.1, 2.8, 0.65, 'Account Created\n(Signal → Student)', C['output'], fontsize=8)
# bottom of Account Created (25.1) → down to 25.625 (mid of Login box) → right to Login left edge
ax.plot([4.6, 4.6], [25.1, 25.625], color=C['auth'], lw=2.0, zorder=2)
arr = FancyArrowPatch((4.6, 25.625), (8.2, 25.625),
                      connectionstyle='arc3,rad=0.0',
                      color=C['auth'], zorder=2, **ARROW_KW)
ax.add_patch(arr)

# YES → straight down
straight_arrow(11, 26.7, 11, 26.0, label='Yes', label_side='right')

# ─────────────────────────────────────────────────────────────────────────────
# LOGIN
# ─────────────────────────────────────────────────────────────────────────────
draw_box(8.2, 25.3, 5.6, 0.65, 'Login\n(Username + Password)', C['auth'], fontsize=9)
straight_arrow(11, 25.3, 11, 24.6)

# ─────────────────────────────────────────────────────────────────────────────
# CREDENTIALS VALID?
# ─────────────────────────────────────────────────────────────────────────────
draw_box(8.2, 23.6, 5.6, 0.9, 'Credentials Valid?', C['decision'], shape='diamond')
straight_arrow(11, 25.3, 11, 24.5)

# INVALID → right loop back
elbow_arrow(13.8, 24.05, 16.5, 24.05, color='#dc2626', via='h-v', label='Invalid')
draw_box(15.5, 23.4, 3.0, 0.65, 'Show Error\nMessage', '#dc2626', fontsize=8.5)
# loop back up to login
ax.plot([18.5, 18.5], [23.4, 25.62], color='#dc2626', lw=2.0, zorder=2)
arr = FancyArrowPatch((18.5, 25.62), (13.8, 25.62),
                      connectionstyle='arc3,rad=0.0',
                      color='#dc2626', zorder=2, **ARROW_KW)
ax.add_patch(arr)
ax.text(16.5, 25.75, 'Retry', fontsize=8, color='#dc2626', fontweight='bold', ha='center')

# VALID → down
straight_arrow(11, 23.6, 11, 22.9, label='Valid', label_side='right')

# ─────────────────────────────────────────────────────────────────────────────
# USER ROLE?
# ─────────────────────────────────────────────────────────────────────────────
draw_box(8.2, 22.0, 5.6, 0.9, 'User Role?', C['decision'], shape='diamond')
straight_arrow(11, 23.6, 11, 22.9)

# ─────────────────────────────────────────────────────────────────────────────
# STUDENT FLOW  (left column  x≈4.5)
# ─────────────────────────────────────────────────────────────────────────────
elbow_arrow(8.2, 22.45, 6.5, 22.45, color=C['student'], via='h-v', label='Student')
draw_box(4.5, 21.7, 4.0, 0.65, 'Student Dashboard', C['student'],
         sublabel='Stats · Charts · Recommendations')
straight_arrow(6.5, 21.7, 6.5, 21.0)

draw_box(4.5, 20.3, 4.0, 0.65, 'Complete Profile', C['student'],
         sublabel='Name · Roll No · Dept · Year · Sem')
straight_arrow(6.5, 20.3, 6.5, 19.6)

draw_box(4.5, 18.9, 4.0, 0.65, 'Enter Marks & Attendance', C['student'],
         sublabel='Per subject: marks/50, attended/total')
straight_arrow(6.5, 18.9, 6.5, 18.2)

draw_box(4.5, 17.5, 4.0, 0.65, 'Save to AcademicRecord DB', C['output'],
         sublabel='update_or_create per subject + internal')
straight_arrow(6.5, 17.5, 6.5, 16.8)

draw_box(4.5, 16.1, 4.0, 0.65, 'Recommendation Engine', C['process'],
         sublabel='Analyse marks per subject')
straight_arrow(6.5, 16.1, 6.5, 15.4)

# MARKS DECISION diamond
draw_box(4.5, 14.5, 4.0, 0.85, 'Marks\nCategory?', C['decision'], shape='diamond')
straight_arrow(6.5, 16.1, 6.5, 15.35)

# Weak  (left)
elbow_arrow(4.5, 14.92, 2.8, 14.92, color='#dc2626', via='h-v', label='<25 Weak')
draw_box(0.5, 14.2, 3.2, 0.7, 'Weak Subject\nBooks + Online\n+ Practice + Strategies',
         '#dc2626', fontsize=8)

# Average (down)
straight_arrow(6.5, 14.5, 6.5, 13.8, color='#b45309', label='25-40 Avg', label_side='right')
draw_box(4.5, 13.1, 4.0, 0.65, 'Average Subject\nGeneral Improvement Tips', '#b45309', fontsize=8)

# Strong (right)
elbow_arrow(8.5, 14.92, 10.2, 14.92, color='#065f46', via='h-v', label='>40 Strong')
draw_box(9.2, 14.2, 3.2, 0.7, 'Strong Subject\nAdvanced Tips\n+ Certifications',
         '#065f46', fontsize=8)

# All three merge down to recommendation page
elbow_arrow(2.1, 14.2, 6.5, 12.55, color='#64748b', via='v-h')
straight_arrow(6.5, 13.1, 6.5, 12.55)
elbow_arrow(10.8, 14.2, 6.5, 12.55, color='#64748b', via='v-h')

draw_box(4.5, 11.85, 4.0, 0.65, 'Display Recommendation Page', C['output'],
         sublabel='student_recommendation.html')

# ─────────────────────────────────────────────────────────────────────────────
# ADMIN FLOW  (right column  x≈15.5)
# ─────────────────────────────────────────────────────────────────────────────
elbow_arrow(13.8, 22.45, 15.5, 22.45, color=C['admin'], via='h-v', label='Admin')
draw_box(13.5, 21.7, 4.0, 0.65, 'Admin Dashboard', C['admin'],
         sublabel='View all students · Search · Filter · Sort')
straight_arrow(15.5, 21.7, 15.5, 21.0)

draw_box(13.5, 20.3, 4.0, 0.65, 'Manage Students', C['admin'],
         sublabel='Add / Edit / Delete Students')
straight_arrow(15.5, 20.3, 15.5, 19.6)

draw_box(13.5, 18.9, 4.0, 0.65, 'Academic Records', C['admin'],
         sublabel='Add / Bulk Upload CSV / View')
straight_arrow(15.5, 18.9, 15.5, 18.2)

draw_box(13.5, 17.5, 4.0, 0.65, 'View Recommendations', C['admin'],
         sublabel='Per student: weak / avg / strong')
straight_arrow(15.5, 17.5, 15.5, 16.8)

draw_box(13.5, 16.1, 4.0, 0.65, 'Analytics Dashboard', C['admin'],
         sublabel='Dept-wise · Subject-wise · Performance')
straight_arrow(15.5, 16.1, 15.5, 15.4)

draw_box(13.5, 14.7, 4.0, 0.65, 'Export PDF Report', C['output'],
         sublabel='Filtered records + performance summary')
straight_arrow(15.5, 14.7, 15.5, 14.0)

draw_box(13.5, 13.3, 4.0, 0.65, 'PDF Downloaded', C['output'],
         sublabel='ReportLab A4 report')

# ─────────────────────────────────────────────────────────────────────────────
# DATABASE LAYER
# ─────────────────────────────────────────────────────────────────────────────
draw_box(6.5, 10.5, 9.0, 0.8, 'Database Layer  (SQLite / PostgreSQL)', C['db'],
         sublabel='Models: Student  |  AcademicRecord  |  User (Django Auth)', fontsize=9.5)

# Student flow → DB
elbow_arrow(6.5, 11.85, 8.5, 11.3, color='#64748b', via='v-h')
# Admin flow → DB
elbow_arrow(15.5, 13.3, 13.5, 11.3, color='#64748b', via='v-h')

# ─────────────────────────────────────────────────────────────────────────────
# SECURITY LAYER
# ─────────────────────────────────────────────────────────────────────────────
draw_box(6.5, 9.3, 9.0, 0.8, 'Security & Middleware', C['security'],
         sublabel='JWT Auth  |  CSRF Protection  |  Input Validation  |  @login_required',
         fontsize=9)
straight_arrow(11, 10.5, 11, 10.1)

# ─────────────────────────────────────────────────────────────────────────────
# LOGOUT
# ─────────────────────────────────────────────────────────────────────────────
draw_box(9, 8.2, 4, 0.65, 'Logout', C['auth'], sublabel='Session Cleared / Token Revoked')
straight_arrow(11, 9.3, 11, 8.85)

# ─────────────────────────────────────────────────────────────────────────────
# END
# ─────────────────────────────────────────────────────────────────────────────
draw_box(9, 7.1, 4, 0.7, 'END', C['end'], fontsize=13, shape='rounded')
straight_arrow(11, 8.2, 11, 7.8)

# ─────────────────────────────────────────────────────────────────────────────
# LEGEND
# ─────────────────────────────────────────────────────────────────────────────
legend_items = [
    (C['start'],    'Start / End'),
    (C['auth'],     'Authentication'),
    (C['decision'], 'Decision (Diamond)'),
    (C['student'],  'Student Flow'),
    (C['admin'],    'Admin Flow'),
    (C['process'],  'Process / Engine'),
    (C['output'],   'Output / Database'),
    ('#dc2626',     'Error / Weak'),
]
lx, ly = 0.3, 10.5
ax.text(lx + 0.25, ly + 0.55, 'LEGEND', fontsize=9.5, fontweight='bold',
        color='#1e3a5f', ha='center')
for i, (color, label) in enumerate(legend_items):
    rect = FancyBboxPatch((lx, ly - i * 0.52), 0.55, 0.35,
                          boxstyle='round,pad=0.05', facecolor=color,
                          edgecolor='white', lw=1.5, zorder=3)
    ax.add_patch(rect)
    ax.text(lx + 0.72, ly - i * 0.52 + 0.175, label,
            fontsize=8.2, va='center', color='#1e293b')

plt.tight_layout(pad=0.5)
plt.savefig('Student_Recommendation_Flowchart.png', dpi=180,
            bbox_inches='tight', facecolor='#f0f4f8')
plt.close()
print("Flowchart saved: Student_Recommendation_Flowchart.png")
