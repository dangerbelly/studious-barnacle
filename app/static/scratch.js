
$(".nav-tabls").on("click","a", function(e){

	e.preventDefault();
	$(this).tab('show');
	})
	.on("click", "span", function(){
		var anchor = $(this).siblings('a');
		$(anchor.att('href')).remove();
		$(this).parent().remove();
        $(".nav-tabs li").children('a').first().click();
    });

    $('.add-contact').click(function(e) {
        e.preventDefault();
        var id = $(".nav-tabs").children().length; //think about it ;)
        $(this).closest('li').before('<li><a href="#contact_'+id+'">New Tab</a><span>x</span></li>');         
        $('.tab-content').append('<div class="tab-pane" id="contact_'+id+'">Contact Form: New Contact '+id+'</div>');
	});

	class GradeYearUploaded(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	gradeyearuploaded = db.Column(db.String(140))
	school = db.Column(db.String(140), db.ForeignKey('uniqueschools.id'))

class AchievementLevelTotals(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	gradeyearuploaded = db.Column(db.String(140), db.ForeignKey('gradeyearsuploaded.id'))
	school = db.Column(db.String(140))
	MathLvl1Total = db.Column(db.Integer)
	MathLvl2Total = db.Column(db.Integer)
	MathLvl3Total = db.Column(db.Integer)
	MathLvl4Total = db.Column(db.Integer)
	ELALvl1Total = db.Column(db.Integer)
	ELALvl2Total = db.Column(db.Integer)
	ELALvl3Total = db.Column(db.Integer)
	ELALvl4Total = db.Column(db.Integer)

	class StudentCounts(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	school = db.Column(db.String(140))
	total_stu_count = db.Column(db.Integer)
	female_count = db.Column(db.Integer)
	male_count = db.Column(db.Integer)
	lim_eng_yes = db.Column(db.Integer)
	lim_eng_no = db.Column(db.Integer)


engine = create_engine(SQLALCHEMY_DATABASE_URI)
metadata = MetaData()
metadata.reflect(engine, only=['table_3rd_14-15'])
Base = automap_base(metadata=metadata)
Base.prepare()
TableThirdFourteenFifteen = Base.classes

'Student First Name'
'Student Last Name'
'Student ID'
'Student DOB'
'Gender'
'Race/Ethnicity'
'IDEA Indicator'
'Limited English Proficiency Status'
'Section 504 Status'
'Economic Disadvantage Status'
'English Language Proficiency Level'
'Language Code'
'Migrant Status'
'First Entry Date Into US School'
'LEP Entry Date'
'LEP Exit Date'
'Primary Disability Type'
'Enrolled Grade'
'Enrolled School'
'Enrolled School ID'
'Enrolled District'
'Enrolled District ID'
'ELA/Literacy OppNumber'
'ELA/Literacy Scale Score'
'Standard Error for ELA/Literacy Scale Score'
'ELA/Literacy Achievement Level'
'Reading Claim Achievement Category'
'Writing Claim Achievement Category'
'Listening Claim Achievement Category'
'Research/Inquiry Claim Achievement Category'
'Mathematics OppNumber'
'Mathematics Scale Score'
'Standard Error for Mathematics Scale Score'
'Mathematics Achievement Level'
'Concepts and Procedures Claim Achievement Category'
'Problem Solving and Modeling & Data Analysis Claim Achievement Category'
'Communicating Reasoning Claim Achievement Category'
