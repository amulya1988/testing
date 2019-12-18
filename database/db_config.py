from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from base_util import config
from database.db_util import gen_relationship, camelize_classname

DB = "DB"

host, user, password, dbname = config.get(DB, 'host'), \
                               config.get(DB, 'user'), \
                               config.get(DB, 'password'), \
                               config.get(DB, 'db')

Base = automap_base()
engine = create_engine(
    'mysql+mysqlconnector://{user}:{password}@{host}/{db}'.format(user=user, password=password, host=host, db=dbname),
    poolclass=NullPool,
    pool_recycle=1800)

# reflect the tables
Base.prepare(engine, reflect=True, classname_for_table=camelize_classname, generate_relationship=gen_relationship)

for c in Base.classes:
    print(c)

AdminView = Base.classes.AdminView
Assessor = Base.classes.Assessor
ProductClientInfoView = Base.classes.ProductClientInfoView
ScoreScale = Base.classes.ScoreScale
BPLeadAssessorCompetencyStatementScore = Base.classes.BPLeadAssessorCompetencyStatementScore
BatchParticipantLeadAssessorMapping = Base.classes.BatchParticipantLeadAssessorMapping
BatchAssessorMapping = Base.classes.BatchAssessorMapping
Batch = Base.classes.Batch
Kit = Base.classes.Kit
Tool = Base.classes.Tool
ProjectManager = Base.classes.ProjectManager
VdcPackage = Base.classes.VdcPackage
CompetencyToolPackage = Base.classes.CompetencyToolPackage
ToolPackage = Base.classes.ToolPackage
BatchParticipantMapper = Base.classes.BatchParticipantMapper
UserInfo = Base.classes.UserInfo
Competency = Base.classes.Competency
CompetencyStatement = Base.classes.CompetencyStatement
BPToolAssessorMapper = Base.classes.BPToolAssessorMapper
BatchToolMapper = Base.classes.BatchToolMapper
ClientToolMapper = Base.classes.ClientToolMapper
ToolPackageDetails = Base.classes.ToolPackageDetails
BPToolAssessorMapperCompetencyStatementScore = Base.classes.BPToolAssessorMapperCompetencyStatementScore
ClientIntegration = Base.classes.ClientIntegration
ClientSuperUser = Base.classes.ClientSuperUser
ClientToolCompetencyMapper = Base.classes.ClientToolCompetencyMapper
CompetencyToolPackageDetails = Base.classes.CompetencyToolPackageDetails
CompetencyToolPackageDetailsScoreText = Base.classes.CompetencyToolPackageDetailsScoreText
Conversation = Base.classes.Conversation
EmailService = Base.classes.EmailService
ReportTemplate = Base.classes.ReportTemplate
ScoreScaleDetails = Base.classes.ScoreScaleDetails
ToolApi = Base.classes.ToolApi
VdcClientMapper = Base.classes.VdcClientMapper

Session = sessionmaker()

Session.configure(bind=engine)


def create_session():
    con = engine.connect()
    session = Session(bind=con)
    return session, con


def close_session(session, con):
    session.close()
    con.close()
