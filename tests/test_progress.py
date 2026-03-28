from socratic_tutor.progress import get_progress_stats, init_progress_db, record_attempt


def test_progress_stats_empty_database(tmp_path):
    db_path = str(tmp_path / "progress.db")
    init_progress_db(db_path)

    stats = get_progress_stats(db_path)
    assert stats["total_attempts"] == 0
    assert stats["total_solved"] == 0
    assert stats["last_7_days"] == 0


def test_progress_record_and_aggregate(tmp_path):
    db_path = str(tmp_path / "progress.db")
    init_progress_db(db_path)

    record_attempt(db_path, "algebra", solved=True, interactions=4)
    record_attempt(db_path, "statistics", solved=False, interactions=3)

    stats = get_progress_stats(db_path)
    assert stats["total_attempts"] == 2
    assert stats["total_solved"] == 1
    assert stats["last_7_days"] >= 2
    assert len(stats["topic_breakdown"]) == 2


def test_progress_common_mistakes_aggregation(tmp_path):
    db_path = str(tmp_path / "progress.db")
    init_progress_db(db_path)

    record_attempt(
        db_path,
        "algebra",
        solved=False,
        interactions=3,
        mistake_tags=["sign_error", "algebra_step_error"],
    )
    record_attempt(
        db_path,
        "algebra",
        solved=False,
        interactions=2,
        mistake_tags=["sign_error"],
    )

    stats = get_progress_stats(db_path)
    assert stats["common_mistakes"][0] == ("sign_error", 2)
    assert ("algebra_step_error", 1) in stats["common_mistakes"]
