from django.db import models


# Create your models here.
class CB22_calibration(models.Model):
    id = models.IntegerField(primary_key=True)
    Date = models.DateTimeField(auto_now_add=True)

    # # Foreign keys to related models
    # WALL = models.ForeignKey(
    #     "WALL_list", on_delete=models.CASCADE
    # )  # ForeignKey to WALL_list
    # CB = models.ForeignKey("CB_list", on_delete=models.CASCADE)  # ForeignKey to CB_list
    # ROB = models.ForeignKey(
    #     "ROB_list", on_delete=models.CASCADE
    # )  # ForeignKey to ROB_list
    # mode = models.ForeignKey(
    #     "Mode_list", on_delete=models.CASCADE
    # )  # ForeignKey to Mode_list
    WALL = models.IntegerField(default=1)
    ROB = models.IntegerField(default=15)
    CB = models.IntegerField(default=22)
    FEB = models.IntegerField(default=61)
    mode = models.IntegerField(default=1)
    Channel = models.IntegerField()
    Chi2NDF = models.CharField(max_length=45)
    N0 = models.CharField(max_length=45)
    Error_N0 = models.CharField(max_length=45)
    Q0 = models.CharField(max_length=45)
    Error_Q0 = models.CharField(max_length=45)
    Q1 = models.CharField(max_length=45)
    Error_Q1 = models.CharField(max_length=45)
    Sigma0 = models.CharField(max_length=45)
    Error_sigma0 = models.CharField(max_length=45)
    Sigma1 = models.CharField(max_length=45)
    Error_sigma1 = models.CharField(max_length=45)
    w = models.CharField(max_length=45)
    Error_w = models.CharField(max_length=45)
    alpha = models.CharField(max_length=45)
    Error_alpha = models.CharField(max_length=45)
    mu = models.CharField(max_length=45)
    Error_mu = models.CharField(max_length=45)
    Chi2NDF_pedestal = models.CharField(max_length=45)
    Chi2NDF_peak = models.CharField(max_length=45)
    Max_Q1_channel = models.CharField(max_length=45)
    gain = models.CharField(max_length=45)
    HV = models.IntegerField()

    class Meta:
        db_table = "cb22_calibration"  # Custom table name
        ordering = ["id"]


# # Create your models here.
# class WALL_list(models.Model):
#     id = models.IntegerField(primary_key=True)
#     WALL = models.IntegerField()

#     class Meta:
#         db_table = "WALL_list"  # Custom table name
#         ordering = ["id"]


# # Create your models here.
# class CB_list(models.Model):
#     id = models.IntegerField(primary_key=True)
#     CB = models.IntegerField()

#     class Meta:
#         db_table = "CB_list"  # Custom table name
#         ordering = ["id"]


# # Create your models here.
# class ROB_list(models.Model):
#     id = models.IntegerField(primary_key=True)
#     ROB = models.IntegerField()

#     class Meta:
#         db_table = "ROB_list"  # Custom table name
#         ordering = ["id"]


# # Create your models here.
# class Mode_list(models.Model):
#     id = models.IntegerField(primary_key=True)
#     mode = models.IntegerField()

#     class Meta:
#         db_table = "mode_list"  # Custom table name
#         ordering = ["id"]
