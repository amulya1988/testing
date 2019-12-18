import pandas as pd
from sqlalchemy.orm import Session

from database.db_config import UserInfo, BatchParticipantMapper


class CrudRepository:
    def __init__(self, session: Session):
        """

        :type session: Session
        """
        self.session = session

    def close_session(self):
        self.session.close()


class UserRepository(CrudRepository):
    def __init__(self, session):
        CrudRepository.__init__(self, session=session)

    def find_bpm_id(self, bpm_id):
        user = self.session.query(UserInfo).join(BatchParticipantMapper).filter(
            BatchParticipantMapper.BPM_ID == bpm_id).first()
        return user


class CompetencyScoreRepository(CrudRepository):

    def __init__(self, session):
        CrudRepository.__init__(self, session=session)

    def find_bplam_score(self, BPM_ID):
        df = pd.read_sql_query(
            "select * from   where BPM_ID={0}".format(BPM_ID),
            self.session.bind)
        df.RATE_AVG = df.RATE_AVG.round(2)
        return df
