from flask import jsonify, g
from sqlalchemy.orm.exc import NoResultFound

from app.libs.error_code import Success, DeleteSuccess, Forbidden
from app.libs.redprint import Redprint
from app.models.base import db
from app.models.question import Question
from app.models.course import Course
from app.models.schedule import Schedule
from app.models.relation import Enroll
from app.validators.forms import CourseCreateForm, CourseUpdateForm, QuestionCreateForm, ScheduleCreateForm, \
    ScheduleUpdateForm
from app.libs.token_auth import auth
from app.libs.enums import UserTypeEnum
from app.models.tag import Tag

api = Redprint('course')


# TODO gid check and scope
@api.route('', methods=['GET'])
def get_course_list():
    return jsonify(courses=Course.query.all())


@api.route('', methods=['POST'])
# @auth.login_required
# @Course.access_scope(UserTypeEnum.MANAGER)
def create_course():
    form = CourseCreateForm().validate_for_api()
    with db.auto_commit():
        course = Course()
        form.populate_obj(course)
        db.session.add(course)
        Enroll.add_user(course, form.teachers_gid.data, form.students_gid.data, form.TAs_gid.data, db)
    return Success()


@api.route('/<int:cid>', methods=['GET'])
def get_course(cid):
    course = Course.query.filter_by(cid=cid).first_or_404()
    return jsonify(course)


@api.route('/<int:cid>', methods=['PUT'])
# @auth.login_required
# @Course.access_scope(UserTypeEnum.TEACHER)
def update_course(cid):
    form = CourseUpdateForm().validate_for_api()
    course = Course.query.filter_by(cid=cid).first_or_404()
    enroll_set = Enroll.query.filter_by(course_cid=cid)
    if enroll_set.count() == 0:
        return Forbidden()
    with db.auto_commit():
        form.populate_obj(course)
        Enroll.add_user(course, form.new_teachers_gid.data, form.new_students_gid.data, form.new_TAs_gid.data, db)
        Enroll.del_user(course, form.del_teachers_gid.data, form.del_students_gid.data, form.del_TAs_gid.data, db)
    return Success()


@api.route('/<int:cid>', methods=['DELETE'])
# @auth.login_required
# @Course.access_scope(UserTypeEnum.MANAGER)
def delete_course(cid):
    course = Course.query.filter_by(cid=cid).first_or_404()
    with db.auto_commit():
        course.delete()
    return DeleteSuccess()


@api.route('/<int:cid>/files', methods=['GET'])
def get_files_list(cid):
    course = Course.query.filter_by(cid=cid).first_or_404()
    return jsonify(files=course.resource)


@api.route('/<int:cid>/questions', methods=['POST'])
# @auth.login_required
def create_question(cid):
    course = Course.query.filter_by(cid=cid).first_or_404()
    form = QuestionCreateForm().validate_for_api()
    with db.auto_commit():
        question = Question(title=form.title.data,
                            content=form.content.data,
                            course_id=course.cid,
                            author_gid='0000000000'
                            )
        for tag_name in form.tags.data:
            tag = Tag.get_or_create_tag(tag_name)
            question.tags.append(tag)
        db.session.add(question)
    return Success()


@api.route('/<int:cid>/questions', methods=['GET'])
def get_question_list(cid):
    course = Course.query.filter_by(cid=cid).first_or_404()
    return jsonify(course.questions)


@api.route('/<int:cid>/schedules', methods=['POST'])
def create_schedule(cid):
    course = Course.query.filter_by(cid=cid).first_or_404()
    form = ScheduleCreateForm().validate_for_api()
    with db.auto_commit():
        schedule = Schedule(week_id=form.week_id.data,
                            topic=form.topic.data,
                            reference=form.reference.data,
                            course_id=course.cid
                            )

        db.session.add(schedule)
    return Success()


@api.route('/<int:cid>/schedules', methods=['GET'])
def list_schedules(cid):
    course = Course.query.filter_by(cid=cid).first_or_404()
    return jsonify(course.schedules)