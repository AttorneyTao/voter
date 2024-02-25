from flask import Blueprint, jsonify, request
from .models import db, Poll, Option, Vote, Voter
from .extensions import db

bp = Blueprint('api', __name__)

@bp.route('/api/polls/<int:poll_id>', methods=['GET'])
def get_poll(poll_id):
    poll = Poll.query.get_or_404(poll_id)
    options = Option.query.filter_by(poll_id=poll.id).all()
    return jsonify({
        'poll': {
            'id': poll.id,
            'title': poll.title,
            'max_votes': poll.max_votes,
            'options': [{'id': option.id, 'title': option.title} for option in options]
        }
    })

@bp.route('/api/vote', methods=['POST'])
def submit_vote():
    data = request.get_json()
    voter_name = data.get('voterName')
    selected_option_ids = data.get('selectedOptions')

    # 检查投票人是否存在
    voter = Voter.query.filter_by(name=voter_name).first()
    if not voter:
        return jsonify({'message': 'invalid voter'}), 404

    # 检查投票人是否已经在任何选项中投过票
    already_voted = Vote.query.join(Option).filter(Vote.voter_name == voter_name, Option.poll_id == data.get('pollId')).first()
    if already_voted:
        # 如果已经投过票，返回重复投票的标志
        return jsonify({'message': 'repeat voting'}), 400

    # 如果没有投过票，记录投票
    for option_id in selected_option_ids:
        vote = Vote(voter_name=voter_name, option_id=option_id)
        db.session.add(vote)
    db.session.commit()

    return jsonify({'message': 'voting success'})

@bp.route('/api/verify-voter', methods=['POST'])
def verify_voter():
    data = request.get_json()
    voter_name = data.get('voterName')
    
    # 在数据库中查找是否存在该投票人
    voter = Voter.query.filter_by(name=voter_name).first()
    
    if voter:
        # 如果找到了投票人，返回验证成功的信息
        return jsonify({'verified': True})
    else:
        # 如果没有找到投票人，返回验证失败的信息
        return jsonify({'verified': False}), 404
    
@bp.route('/api/poll-results/<int:poll_id>')
def poll_results(poll_id):
    # 获取指定poll_id的所有选项及其票数
    options = Option.query.filter_by(poll_id=poll_id).all()
    
    results = []
    for option in options:
        # 对于每个选项，计算其获得的票数
        vote_count = Vote.query.filter_by(option_id=option.id).count()
        results.append({'option_id': option.id, 'title': option.title, 'votes': vote_count})
    
    return jsonify({'poll_id': poll_id, 'results': results})

@bp.route('/api/has-voted', methods=['POST'])
def has_voted():
    data = request.get_json()
    voter_name = data.get('voterName')
    poll_id = data.get('pollId')
    
    # 查询给定poll_id和voter_name的Vote记录
    vote = Vote.query.join(Option, Vote.option_id == Option.id).filter(Option.poll_id == poll_id, Vote.voter_name == voter_name).first()
    
    if vote:
        # 如果找到了匹配的投票记录，返回已投票的信息
        return jsonify({'hasVoted': True})
    else:
        # 如果没有找到匹配的投票记录，返回未投票的信息
        return jsonify({'hasVoted': False})
@bp.route('/api/clear-votes', methods=['POST'])
def clear_votes():
    try:
        # 删除Vote表中的所有记录
        num_rows_deleted = db.session.query(Vote).delete()
        db.session.commit()
        return jsonify({'message': f'Successfully deleted {num_rows_deleted} votes.'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500